import os
import requests
import django
import nltk

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eeet2582_backend.settings')
django.setup()

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_title import DocumentTitle
from eeet2582_backend.api.models.endnote import EndNote
from eeet2582_backend.api.models.heading import Heading
from eeet2582_backend.api.models.list_paragraph import ListParagraph
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.api.models.document_table import DocumentTable
from eeet2582_backend.api.models.table_row import TableRow
from eeet2582_backend.api.models.row_cell import RowCell

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def correct_text(text):
    api_endpoint = "https://polite-horribly-cub.ngrok-free.app/generate_code"
    params = {
        'prompts': f'Correct English:{text} Here is the corrected version:'
    }
    return requests.get(api_endpoint, params=params)

def process_docx():
    user_doc = UserDocument.objects.latest('created_at')
    process_title(user_doc)
    process_paragraph(user_doc)
    process_heading(user_doc)
    process_endnote(user_doc)

def process_title(user_doc):
    titles = DocumentTitle.objects.filter(userdocument=user_doc).order_by('id')

    for title in titles:
        if title.title:
            response = correct_text(title.title)
            if response.status_code == 200:
                corrected_text = response.json()[0].strip()
                title.title = corrected_text
                title.save()
            else:
                print("Error: ", response.status_code)
                return

def process_paragraph(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    for paragraph in paragraphs:
        if paragraph.content:
            corrected_paragraph = ""
            sentences = sent_tokenize(paragraph.content)

            for sentence in sentences:
                # print(sentence)
                response = correct_text(sentence)
                if response.status_code == 200:
                    corrected_text = response.json()[0].strip()
                    # print(corrected_text)
                    corrected_paragraph += corrected_text + " "
                else:
                    print("Error: ", response.status_code)
                    return
            # print(corrected_paragraph)
            paragraph.content = corrected_paragraph
            paragraph.save()
    
def process_heading(user_doc):
    headings = Heading.objects.filter(user_document=user_doc).order_by('id')

    for heading in headings:
        if heading.content:
            corrected_heading = ""
            sentences = sent_tokenize(heading.content)

            for sentence in sentences:
                # print(sentence)
                response = correct_text(sentence)
                if response.status_code == 200:
                    corrected_text = response.json()[0].strip()
                    corrected_heading += corrected_text + " "
                else:
                    print("Error: ", response.status_code)
                    return
            heading.content = corrected_heading
            heading.save()

def process_endnote(user_doc):
    endnotes = EndNote.objects.filter(user_document=user_doc).order_by('id')

    for endnote in endnotes:
        if endnote.content:
            response = correct_text(endnote.content)
            if response.status_code == 200:
                corrected_text = response.json()[0].strip()
                endnote.content = corrected_text
                endnote.save()
            else:
                print("Error: ", response.status_code)
                return

process_docx()