import re
import requests
from celery import group, chord

from eeet2582_backend.api.models.document_paragraph import DocumentParagraph
from eeet2582_backend.api.models.document_paragraph_result import DocumentParagraphResult
from eeet2582_backend.api.models.user_document import UserDocument
from eeet2582_backend.celery import app
from celery.result import GroupResult

from .parse_docx import ParseDocxService
from .return_docx import ReturnDocxService


def correct_text(text):
    text = re.sub(' +', ' ', text)  # remove extra spaces
    endsproperly = text.endswith('.') or text.endswith('?') or text.endswith('!')

    api_endpoint = "https://polite-horribly-cub.ngrok-free.app/generate_code"
    params = {
        'prompts': f'Correct English:{text if endsproperly else text + '.'}Here is the corrected version no explaination:',
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
        if (abs(len(result) - len(text)) > 10):
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
def process_user_doc(file_path, current_user_id):
    docx_parser = ParseDocxService(file_path, current_user_id)
    parsed_docx_id = docx_parser.parse()

    user_doc = UserDocument.objects.get(id=parsed_docx_id)

    if not user_doc:
        return 'No document found'

    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    result = chord(correct_text_paragraph.s(paragraph.id) for paragraph in paragraphs)(ReturnDocxService.create_docx.s(
        user_doc.id, file_path))

    return result.id


@app.task
def process_docx(user_doc_id):
    group_result_id = process_user_doc.apply_async([user_doc_id])

    result = GroupResult.restore(group_result_id)

    if result.ready():
        return "Everything is done"
    else:
        return "Still processing." + str(result.completed_count()) + " out of " + str(result.total_count())


@app.task
def process_latest_docx(self):
    user_doc = UserDocument.objects.latest('created_at')

    if not user_doc:
        return 'No document found'

    result = process_docx.apply_async([user_doc.id])
    return result


def process_docx_old():
    user_doc = UserDocument.objects.latest('created_at')
    process_paragraph_old(user_doc)


def process_paragraph_old(user_doc):
    paragraphs = DocumentParagraph.objects.filter(user_document=user_doc).order_by('id')

    for paragraph in paragraphs:
        if paragraph.content:
            paragraph_result = DocumentParagraphResult.objects.create(original_paragraph=paragraph)
            paragraph_result.content = correct_text(paragraph.content)
            paragraph_result.save()
