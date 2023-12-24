import os
from docx import Document
from eeet2582_backend.models import DocumentTitle, UserDocument, DocumentParagraph, Heading, EndNote, ListParagraph

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

    for para in paragraphs:
        related_headings = headings.filter(document_paragraph=para)
        related_list_paragraphs = list_paragraphs.filter(document_paragraph=para)
        has_heading = related_headings.exists()
        has_list_paragraph = related_list_paragraphs.exists()
        
        # Case both heading and list paragraph with paragraph (ID equal)
        if has_heading and has_list_paragraph:
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
            doc.add_paragraph(para.content)
            for list_para in related_list_paragraphs:
                doc.add_paragraph(list_para.content, style='List Bullet')
        # Case heading with paragraph (ID equal)
        elif has_heading:
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
            doc.add_paragraph(para.content)
        # Case List paragraph with paragraph (ID equal)
        elif has_list_paragraph:
            doc.add_paragraph(para.content)
            for list_para in related_list_paragraphs:
                doc.add_paragraph(list_para.content, style='List Bullet')
        # Case paragraph stand alone
        else:
            doc.add_paragraph(para.content)

    # Case Headings without paragraphs
    standalone_headings = headings.filter(document_paragraph__isnull=True)
    for heading in standalone_headings:
        doc.add_heading(heading.content, level=1)

    # Add endnotes
    for endnote in EndNote.objects.filter(user_document=user_doc):
        doc.add_paragraph(endnote.content)

    # Save the document
    # The filename is based on the document title;
    # Replace 'desired_path' with the actual path
    filename = "".join([c for c in doc_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    save_path = f"output_docx/{filename}.docx"  
    doc.save(save_path)