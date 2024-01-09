from docx import Document
from docx.document import Document as doctwo
import re

from eeet2582_backend.models import *

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_title import DocumentTitle
from eeet2582_backend.api.models.endnote import EndNote
from eeet2582_backend.api.models.heading import Heading
from eeet2582_backend.api.models.caption import Caption
from eeet2582_backend.api.models.list_paragraph import ListParagraph
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.api.models.subheading import Subheading
from eeet2582_backend.api.models.document_table import DocumentTable
from eeet2582_backend.api.models.table_row import TableRow
from eeet2582_backend.api.models.row_cell import RowCell
from eeet2582_backend.api.models.document_image import DocumentImage
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.oxml.shape import CT_Picture, CT_Inline
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from io import StringIO
import base64


from ..api.models.user_model import User


class ParseDocxService:
    heading_pattern = re.compile(r"Heading \d")

    def __init__(self, file_path, current_user_id):
        self.file_path = file_path
        self.user_id = current_user_id
    def parse(self):
        document = Document(self.file_path)
        document_instance = None
        document_title = None
        current_paragraph = None
        imagecounter = 0

        current_user = User.objects.get(id=self.user_id)

        for element in document.element.body:
            # Case 1: Paragraph
            if isinstance(element, CT_P):
                paragraph = Paragraph(element, document)

                for run in paragraph.runs:
                    xmlstr = str(run.element.xml)
                    my_namespaces = dict([node for _, node in ElementTree.iterparse(StringIO(xmlstr), events=['start-ns'])])
                    root = ET.fromstring(xmlstr) 
                    #Check if pic is there in the xml of the element. If yes, then extract the image data
                    if 'pic:pic' in xmlstr:
                        print("ImageFound")
                        for pic in root.findall('.//pic:pic', my_namespaces):
                            print("ImageFound 2")
                            cNvPr_elem = pic.find("pic:nvPicPr/pic:cNvPr", my_namespaces)
                            name_attr = cNvPr_elem.get("name")
                            blip_elem = pic.find("pic:blipFill/a:blip", my_namespaces)
                            embed_attr = blip_elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")  
                            document_part = document.part
                            image_part = document_part.related_parts[embed_attr]
                            image_base64 = base64.b64encode(image_part._blob)
                            image_base64 = image_base64.decode()     
                            if not current_paragraph:    
                                DocumentImage.objects.create(user_document=document_instance, document_paragraph=None, file_name=name_attr,  content=image_base64)
                            elif current_paragraph:     
                                DocumentImage.objects.create(user_document=document_instance, document_paragraph=current_paragraph, file_name=name_attr,  content=image_base64)    
                            imagecounter = imagecounter + 1
                if paragraph.text.strip() and not document_title:
                    document_title = DocumentTitle.objects.create(title=paragraph.text)

                    document_instance = UserDocument.objects.create(document_title=document_title, user=current_user)
                    continue

                elif document_instance:
                    paragraph_content = paragraph.text.strip()

                    if paragraph_content:
                        # check if the paragraph is a heading
                        if re.match(self.heading_pattern, paragraph.style.name):

                            # handle subheadings
                            headings_without_paragraphs = Heading.objects.filter(user_document=document_instance,
                                                                                 document_paragraph=None)

                            if headings_without_paragraphs.exists():
                                Subheading.objects.create(
                                    heading=headings_without_paragraphs.first(),
                                    content=paragraph_content,
                                    type=paragraph.style.name)
                                continue
                            else:
                                Heading.objects.create(user_document=document_instance, content=paragraph_content)
                            continue

                        if paragraph.style.name == 'List Paragraph':
                            # if there is no current paragraph, then we get the last paragraph
                            if not current_paragraph:
                                current_paragraph = DocumentParagraph.objects.filter(
                                    user_document=document_instance).last()
                                continue

                            ListParagraph.objects.create(user_document=document_instance,
                                                         document_paragraph=current_paragraph,
                                                         content=paragraph_content)
                            continue

                        if paragraph.style.name == 'Normal' or paragraph.style.name == 'Normal (Web)':
                            # first check if there is a heading before this paragraph
                            headings_without_paragraphs = Heading.objects.filter(user_document=document_instance,
                                                                                 document_paragraph=None)

                            if headings_without_paragraphs.exists():
                                orphan_heading = headings_without_paragraphs.first()
                                # if there is a heading without a paragraph, then we assign the paragraph to that
                                # heading
                                current_paragraph = DocumentParagraph.objects.create(
                                    user_document=document_instance, content=paragraph_content)

                                orphan_heading.document_paragraph = current_paragraph
                                orphan_heading.save()
                            else:
                                current_paragraph = DocumentParagraph.objects.create(user_document=document_instance,
                                                                                     content=paragraph_content)
                        if paragraph.style.name == 'Caption':
                            Caption.objects.create(user_document = document_instance, document_paragraph = current_paragraph, content = paragraph_content)

                    if paragraph.style.name == 'EndNote Bibliography':
                        EndNote.objects.create(user_document=document_instance, content=paragraph_content)
                        continue
            elif isinstance(element, CT_Tbl):
                if document_instance is None:
                    continue  # Or handle the case where no document_instance is found
                # Create a DocumentTable instance for each table in the document
                table = Table(element, document)
                if current_paragraph:
                    document_table = DocumentTable.objects.create(user_document=document_instance,
                                                                  document_paragraph=current_paragraph, content="")
                else:
                    document_table = DocumentTable.objects.create(user_document=document_instance, content="")
                for i, row in enumerate(table.rows):
                    # Create a TableRow instance for each row in the table
                    table_row = TableRow.objects.create(user_document=document_instance, document_table=document_table,
                                                        content="")

                    for cell in row.cells:
                        # Extract content from each cell
                        cell_content = cell.text.strip()

                        # Create a RowCell instance for each cell in the row
                        RowCell.objects.create(user_document=document_instance, document_table=document_table, table_row=table_row, content=cell_content)
            elif isinstance(element, CT_Inline):
            # else:
                print("image found 11")
                # xmlstr = str(element.xml)
                # root = etree.fromstring(xmlstr)
                # # if element.tag.endswith('}drawing'):
                # # Extract image logic here
                # image_part = element.find('.//a:blip', namespaces=nsmap)
                # if image_part is not None:
                #     image_id = image_part.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed']
                #     image_data = document.part.related_parts[image_id]._blob  # Binary image data
                #     # Process image_data as needed (save, convert, etc.)
                #     DocumentImage.objects.create(user_document=document_instance, document_paragraph=current_paragraph, file_name=f"image_{image_no}", content = image_data) 
                #     image = Image.open(BytesIO(image_data))
                #     image.save(f"extracted_image{image_no}.png")
                #     image_no = image_no + 1
        
        return document_instance.id
