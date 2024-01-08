import re
import requests
from celery import group

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_paragraph_result import DocumentParagraphResult
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.celery import app

def correct_text(text):
    text = re.sub(' +', ' ', text) # remove extra spaces
    endsproperly = text.endswith('.') or text.endswith('?') or text.endswith('!')

    api_endpoint = "https://polite-horribly-cub.ngrok-free.app/generate_code"
    params = {
        'prompts': f'Correct English:{text if endsproperly else text+'.'}Here is the corrected version no explaination:',
        'max_length': len(text)
    }

    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        result = response.json()[0]
        
        # format the corrected text
        result = re.sub('Correct English: ', '', result)
        result = re.sub(' +', ' ', result)
        result = re.sub('\n', '', result)
        result = result if endsproperly else result[:-1]

        # return orignal text if the correction is too different
        if(abs(len(result) - len(text)) > 10):
            return text

        return result
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