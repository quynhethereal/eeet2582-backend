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
    process_paragraph(user_doc)

def process_paragraph(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    paragraph = paragraphs[7]
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
        print(corrected_paragraph)

    # for paragraph in paragraphs:
    #     if paragraph.content:
    #         corrected_paragraph = ""
    #         sentences = sent_tokenize(paragraph.content)

    #         for sentence in sentences:
    #             # print(sentence)
    #             response = correct_text(sentence)
    #             if response.status_code == 200:
    #                 corrected_text = response.json()[0].strip()
    #                 # print(corrected_text)
    #                 corrected_paragraph += corrected_text + " "
    #             else:
    #                 print("Error: ", response.status_code)
    #         # print(corrected_paragraph)
    #         paragraph.content = corrected_paragraph
    #         paragraph.save()

process_docx()