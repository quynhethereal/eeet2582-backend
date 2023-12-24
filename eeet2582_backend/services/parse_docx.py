from docx import Document
import re

from eeet2582_backend.models import *


class ParseDocxService:
    heading_pattern = re.compile(r"Heading \d")

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        document = Document(self.file_path)
        document_instance = None
        document_title = None
        current_paragraph = None
        document_table = None
        
        for paragraph in document.paragraphs:
            # extract title from the first paragraph that is not empty
            if paragraph.text.strip() and not document_title:
                document_title = DocumentTitle.objects.create(title=paragraph.text)

                document_instance = UserDocument.objects.create(document_title=document_title)
                continue
                # return document_instance


            elif document_instance:
                paragraph_content = paragraph.text.strip()

                if paragraph_content:
                    if re.match(self.heading_pattern, paragraph.style.name):
                        Heading.objects.create(user_document=document_instance, content=paragraph_content)

                        # import pdb; pdb.set_trace()
                        continue

                    if paragraph.style.name == 'List Paragraph':
                        # if there is no current paragraph, then we get the last paragraph
                        if not current_paragraph:
                            current_paragraph = DocumentParagraph.objects.filter(user_document=document_instance).last()
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
                            # if there is a heading without a paragraph, then we assign the paragraph to that heading
                            current_paragraph = DocumentParagraph.objects.create(
                                user_document=document_instance, content=paragraph_content)

                            orphan_heading.document_paragraph = current_paragraph
                            orphan_heading.save()
                        else:
                            current_paragraph = DocumentParagraph.objects.create(user_document=document_instance,
                                                                                 content=paragraph_content)

                        continue

                    if paragraph.style.name == 'EndNote Bibliography':
                        EndNote.objects.create(user_document=document_instance, content=paragraph_content)
                        continue
        for table in document.tables:
            if document_instance is None:
            # Ensure document_instance is created before processing tables
                continue  # Or handle the case where no document_instance is found
            
            # Create a DocumentTable instance for each table in the document
            document_table = DocumentTable.objects.create(user_document=document_instance, content="")

            for i, row in enumerate(table.rows):
                # Create a TableRow instance for each row in the table
                table_row = TableRow.objects.create(user_document=document_instance, document_table=document_table, content="")

                for cell in row.cells:
                    # Extract content from each cell
                    cell_content = cell.text.strip()

                    # Create a RowCell instance for each cell in the row
                    RowCell.objects.create(user_document=document_instance, document_table=document_table, table_row=table_row, content=cell_content)
        return None
