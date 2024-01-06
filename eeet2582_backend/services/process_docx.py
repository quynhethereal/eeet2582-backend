import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eeet2582_backend.settings')
django.setup()

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_paragraph_result import DocumentParagraphResult
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.celery import app

from celery import chord , group

def correct_text(text):
    endswithcolon = not text.endswith('.') or not text.endswith('?') or not text.endswith('!')

    api_endpoint = "https://polite-horribly-cub.ngrok-free.app/generate_code"
    params = {
        'prompts': f'Correct English:{text+'.' if endswithcolon else text}Here is the corrected version no explaination:',
        'max_length': len(text)
    }

    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()[0].strip()[:-1] if endswithcolon else response.json()[0].strip()
    else:
        return text
    
@app.task
def correct_text_paragraph(paragraph_id):
    paragraph = DocumentParagraph.objects.get(id=paragraph_id)
    paragraph_result = DocumentParagraphResult.objects.create(original_paragraph=paragraph)
    if paragraph.content:
        # print(paragraph.content)
        result = correct_text(paragraph.content)
        paragraph_result.content = result
        paragraph_result.save()
        return result

@app.task
def process_paragraph():
    user_doc = UserDocument.objects.latest('created_at')
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    # result = chord(correct_text_paragraph.s(paragraph.id) for paragraph in paragraphs)

    result = group(correct_text_paragraph.s(paragraph.id) for paragraph in paragraphs).apply_async()
    return result

@app.task
def process_docx():
    result = process_paragraph.apply_async()
    return result

def process_docx_old():
    user_doc = UserDocument.objects.latest('created_at')
    process_paragraph_old(user_doc)

def process_paragraph_old(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')
    paragraph_result = DocumentParagraphResult.objects.create(original_paragraph=paragraph)

    for paragraph in paragraphs:
        if paragraph.content:
            paragraph_result.content = correct_text(paragraph.content)
            paragraph_result.save()