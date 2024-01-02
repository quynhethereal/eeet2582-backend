
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


# Function remove invalid characters in filename
def remove_invalid(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

# Function add heading to the document
def add_headings(doc, heading_content, level):
    doc.add_heading(heading_content, level)

# Function add paragraph to the document
def add_paragraphs(doc, content):
    doc.add_paragraph(content)

# Fucntion add a list of paragraph to the document
def add_list_paragraph(doc, content):
    doc.add_paragraph(content, style='List Bullet')

# Function add table to the document
def add_table_to_doc(doc, table):
    if not table.tablerow_set.exists():
        return

    # Determine the number of columns
    number_of_columns = len(table.tablerow_set.first().rowcell_set.all())
    doc_table = doc.add_table(rows=0, cols=number_of_columns)
    doc_table.style = 'Table Grid'

    # Add rows and cells to the table
    for row in table.tablerow_set.all():
        cells = row.rowcell_set.all()
        row_cells = doc_table.add_row().cells
        for idx, cell in enumerate(cells):
            row_cells[idx].text = cell.content

# Function create word docx document
def create_docx():
    user_doc = UserDocument.objects.latest('created_at')
    # Create a new Word document
    doc = Document()

    # Add the title to the document
    doc_title = user_doc.document_title.title
    add_headings(doc, doc_title, level=0)

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
                add_headings(doc, heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                add_headings(doc, subheading.content, level=subheading_level)    
            add_paragraphs(doc, para.content)
            #list paragraph
            for list_para in related_list_paragraphs:
                add_list_paragraph(doc, list_para.content)
        # Case both heading and table with paragraph (ID equal)
        elif has_heading and has_table:
            for heading in related_headings:
                add_headings(doc, heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                add_headings(doc, subheading.content, level=subheading_level)
            add_paragraphs(doc, para.content)
            for table in related_tables:
                add_table_to_doc(doc, table)
        # Case heading with paragraph (ID equal)
        elif has_heading:
            for heading in related_headings:
                add_headings(doc, heading.content, level=1)
            # Subheading
            related_subheadings = Subheading.objects.filter(heading=heading)
            for subheading in related_subheadings:
                subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
                add_headings(doc, subheading.content, level=subheading_level)
            add_paragraphs(doc, para.content)
        # Case List paragraph with paragraph (ID equal)
        elif has_list_paragraph:
            add_paragraphs(doc, para.content)
            for list_para in related_list_paragraphs:
                add_list_paragraph(doc, list_para.content)
        # Case table with paragraph (ID equal)
        elif has_table:
            add_paragraphs(doc, para.content)
            for table in related_tables:
                add_table_to_doc(doc, table)
        # Case paragraph stand alone
        else:
            add_paragraphs(doc, para.content)

    # Case Headings without paragraphs
    standalone_headings = headings.filter(document_paragraph__isnull=True)
    for heading in standalone_headings:
        add_headings(doc, heading.content, level=1)
    # Subheading
    related_subheadings = Subheading.objects.filter(heading=heading)
    for subheading in related_subheadings:
        subheading_level = int(re.search(r'\d+', subheading.type).group()) if re.search(r'\d+', subheading.type) else 2
        add_headings(doc, subheading.content, level=subheading_level)
        
    # Add endnotes
    for endnote in EndNote.objects.filter(user_document=user_doc):
        add_paragraphs(doc, endnote.content)

    # Save the document
    # The filename is based on the document title;
    # Replace 'desired_path' with the actual path
    save_path = f"output_docx/{remove_invalid(doc_title)}.docx"
    doc.save(save_path)
