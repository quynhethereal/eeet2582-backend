import os
from docx import Document
from eeet2582_backend.models import DocumentTitle, UserDocument, DocumentParagraph, Heading, EndNote

def create_docx():
    user_doc = UserDocument.objects.latest('created_at')
    # Create a new Word document
    doc = Document()

    # Add the title to the document
    doc_title = user_doc.document_title.title
    doc.add_heading(doc_title, level=0)

    # Fetch and sort headings and paragraphs
    headings = Heading.objects.filter(user_document=user_doc)
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

     # Case 1: Paragraphs without headings
    for para in paragraphs:
        if not headings.filter(document_paragraph=para).exists():
            doc.add_paragraph(para.content)
        else:
            # Case 2: Headings with paragraphs
            related_headings = headings.filter(document_paragraph=para)
            for heading in related_headings:
                doc.add_heading(heading.content, level=1)
                doc.add_paragraph(para.content)

    # Case 3: Headings without paragraphs
    standalone_headings = headings.filter(document_paragraph__isnull=True)
    for heading in standalone_headings:
        doc.add_heading(heading.content, level=1)

    # # The sorting mechanism depends on whether the Heading is associated with a DocumentParagraph
    # sorted_items = []
    # for para in paragraphs:
    #     related_headings = headings.filter(document_paragraph=para)
    #     for heading in related_headings:
    #         sorted_items.append(('heading', heading))
    #     sorted_items.append(('paragraph', para))

    # # Add headings without a document_paragraph (those come before the endnotes)
    # standalone_headings = headings.filter(document_paragraph__isnull=True)
    # for heading in standalone_headings:
    #     sorted_items.append(('heading', heading))

    # # Add sorted headings and paragraphs to the document
    # for item_type, item in sorted_items:
    #     if item_type == 'heading':
    #         doc.add_heading(item.content, level=1)  # Add as heading with level 1
    #     elif item_type == 'paragraph':
    #         doc.add_paragraph(item.content)

    # Add endnotes
    for endnote in EndNote.objects.filter(user_document=user_doc):
        doc.add_paragraph(endnote.content)

    # Save the document
    # The filename is based on the document title;
    # Replace 'desired_path' with the actual path
    filename = "".join([c for c in doc_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    save_path = f"output_docx/{filename}.docx"  
    doc.save(save_path)