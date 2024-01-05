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
from eeet2582_backend.celery import app

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

@app.task
def correct_text(text):
    api_endpoint = "https://polite-horribly-cub.ngrok-free.app/generate_code"
    params = {
        'prompts': f'Correct English:{text} Here is the corrected version:'
    }
    response = requests.get(api_endpoint, params=params)
    if(response.status_code == 200):
        return response.json()[0].strip()
    else:
        return text;

@app.task
def correct_text_paragraph(paragraph_id):
    paragraph = DocumentParagraph.objects.get(id=paragraph_id)
    if paragraph.content:
        corrected_paragraph = ""
        sentences = sent_tokenize(paragraph.content)
        for sentence in sentences:
            corrected_paragraph += correct_text.delay(sentence) + " "
        paragraph.content = corrected_paragraph
        paragraph.save()

def process_paragraph(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    for paragraph in paragraphs:
        correct_text_paragraph.delay(paragraph.id)

@app.task
def process_docx():
    user_doc = UserDocument.objects.latest('created_at')
    process_paragraph(user_doc)

def process_docx_old():
    user_doc = UserDocument.objects.latest('created_at')
    process_title(user_doc)
    process_paragraph_old(user_doc)
    process_heading(user_doc)
    process_endnote(user_doc)

def process_title(user_doc):
    titles = DocumentTitle.objects.filter(userdocument=user_doc).order_by('id')

    for title in titles:
        if title.title:
            title.title = correct_text(title.title)
            title.save()

def process_paragraph_old(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    for paragraph in paragraphs:
        if paragraph.content:
            corrected_paragraph = ""
            sentences = sent_tokenize(paragraph.content)

            for sentence in sentences:
                # print(sentence)
                corrected_paragraph += correct_text(sentence) + " "
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
                corrected_heading += correct_text(sentence) + " "
            heading.content = corrected_heading
            heading.save()

def process_endnote(user_doc):
    endnotes = EndNote.objects.filter(user_document=user_doc).order_by('id')

    for endnote in endnotes:
        if endnote.content:
            endnote.content = correct_text(endnote.content)
            endnote.save()
            
process_docx_old()