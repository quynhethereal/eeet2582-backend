from docx import Document
import re

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_title import DocumentTitle
from eeet2582_backend.api.models.heading import Heading
from eeet2582_backend.api.models.user_document import UserDocument


class ParseDocxService:
    heading_pattern = re.compile(r"Heading \d")

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        document = Document(self.file_path)
        document_instance = None
        document_title = None

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
                    if paragraph.style.name == 'Normal':
                        # first check if there is a heading before this paragraph
                        headings_without_paragraphs = Heading.objects.filter(user_document=document_instance,
                                                                             document_paragraph=None)

                        if headings_without_paragraphs.exists():
                            orphan_heading = headings_without_paragraphs.first()
                            # if there is a heading without a paragraph, then we assign the paragraph to that heading
                            orphan_heading.document_paragraph = DocumentParagraph.objects.create(
                                user_document=document_instance, content=paragraph_content)
                            orphan_heading.save()
                        else:
                            DocumentParagraph.objects.create(user_document=document_instance, content=paragraph_content)

        return None
