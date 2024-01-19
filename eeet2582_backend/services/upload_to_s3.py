import os
import boto3
from django.conf import settings
from io import BytesIO


def upload_to_s3(doc, file_path):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    doc_io = BytesIO()
    doc.save(doc_io)
    normalized_path = os.path.normpath(file_path)
    file_name = os.path.split(normalized_path)[-1]

    # Reset the BytesIO cursor position to the beginning
    doc_io.seek(0)
    # Initialize the S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        # Upload the file object directly to S3
        s3.upload_fileobj(doc_io, bucket_name, f"fixed_{file_name}")
        os.remove(file_path)
        return f"fixed_{file_name}"
    except Exception as e:
        # Handle any exceptions that might occur during the upload
        print("Error uploading file to S3:", e)
        return 'Failed to upload file'