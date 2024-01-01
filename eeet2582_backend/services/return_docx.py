
import re
from docx import Document

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_title import DocumentTitle
from eeet2582_backend.api.models.endnote import EndNote
from eeet2582_backend.api.models.heading import Heading
from eeet2582_backend.api.models.list_paragraph import ListParagraph
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.api.models.subheading import Subheading
from eeet2582_backend.api.models.document_table import DocumentTable
from eeet2582_backend.api.models.table_row import TableRow
from eeet2582_backend.api.models.row_cell import RowCell

def create_docx():
    user_doc = UserDocument.objects.latest('created_at')
    # Create a new Word document
    doc = Document()

    # Add the title to the document
    doc_title = user_doc.document_title.title
    doc.add_heading(doc_title, level=0)

    # Fetch and sort headings and paragraphs
    headings = Heading.objects.filter(user_document=user_doc)
    list_paragraphs = ListParagraph.objects.filter(user_document=user_doc)
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')
    tables = DocumentTable.objects.filter(user_document=user_doc)

    for para in paragraphs:
        related_headings = headings.filter(document_paragraph=para)
        related_list_paragraphs = list_paragraphs.filter(document_paragraph=para)
        related_tables = tables.filter(document_paragraph=para)
        
        has_heading = related_headings.exists()
        has_list_paragraph = related_list_paragraphs.exists()
        has_table = related_tables.exists()

        # Case both heading and list paragraph with paragraph (ID equal)
        if has_heading and has_list_paragraph:
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                doc.add_heading(subheading.content, level=subheading_level)    
            doc.add_paragraph(para.content)
            #list paragraph
            for list_para in related_list_paragraphs:
                doc.add_paragraph(list_para.content, style='List Bullet')
        # Case both heading and table with paragraph (ID equal)
        elif has_heading and has_table:
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                doc.add_heading(subheading.content, level=subheading_level)
            doc.add_paragraph(para.content)
            for table in related_tables:
                doc_table = doc.add_table(rows=0, cols=len(table.tablerow_set.first().rowcell_set.all()))
                doc_table.style = 'Table Grid'
                # Add the content from the table rows and cells
                for row in table.tablerow_set.all():
                    cells = row.rowcell_set.all()
                    row_cells = doc_table.add_row().cells
                    for idx, cell in enumerate(cells):
                        row_cells[idx].text = cell.content
        # Case heading with paragraph (ID equal)
        elif has_heading:
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                doc.add_heading(subheading.content, level=subheading_level)
            doc.add_paragraph(para.content)
        # Case List paragraph with paragraph (ID equal)
        elif has_list_paragraph:
            doc.add_paragraph(para.content)
            for list_para in related_list_paragraphs:
                doc.add_paragraph(list_para.content, style='List Bullet')
        # Case table with paragraph (ID equal)
        elif has_table:
            doc.add_paragraph(para.content)
            for table in related_tables:
                doc_table = doc.add_table(rows=0, cols=len(table.tablerow_set.first().rowcell_set.all()))
                doc_table.style = 'Table Grid'
                # Add the content from the table rows and cells
                for row in table.tablerow_set.all():
                    cells = row.rowcell_set.all()
                    row_cells = doc_table.add_row().cells
                    for idx, cell in enumerate(cells):
                        row_cells[idx].text = cell.content
        # Case paragraph stand alone
        else:
            doc.add_paragraph(para.content)

    # Case Headings without paragraphs
    standalone_headings = headings.filter(document_paragraph__isnull=True)
    for heading in standalone_headings:
        doc.add_heading(heading.content, level=1)
    # Subheading
    related_subheadings = Subheading.objects.filter(heading=heading)
    for subheading in related_subheadings:
        subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
        doc.add_heading(subheading.content, level=subheading_level)
        
    # Add endnotes
    for endnote in EndNote.objects.filter(user_document=user_doc):
        doc.add_paragraph(endnote.content)

    # Save the document
    # The filename is based on the document title;
    # Replace 'desired_path' with the actual path
    filename = "".join([c for c in doc_title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    save_path = f"output_docx/{filename}.docx"
    doc.save(save_path)
