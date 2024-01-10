import os
import boto3

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from eeet2582_backend.services.parse_docx import ParseDocxService
from eeet2582_backend.celery import app


class ParseDocxAPIView(APIView):
    # TODO: Enable authentication and permissions
    authentication_classes = []
    permission_classes = []

    @app.task
    def parse_docx_task(file_path):
        docx_parser = ParseDocxService(file_path)
        result = docx_parser.parse()
        return result
    
    def post(self, request):
        if request.method == 'POST' and request.FILES.get('docx_file'):
            file_obj = request.FILES['docx_file']
            # Get AWS credentials and bucket name from Django settings
            AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
            AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            # Initialize the S3 client
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            try:
                # Upload the file object directly to S3
                s3.upload_fileobj(file_obj, bucket_name, file_obj.name)
                # Optionally, you might want to save some metadata to your database here
                result = self.parse_docx_task.delay(f"https://group1-bucket.s3.ap-southeast-1.amazonaws.com/{file_obj.name}")
                return Response({"file_name": result}, status=200)
            except Exception as e:
                # Handle any exceptions that might occur during the upload
                print("Error uploading file to S3:", e)
                return Response({'error': 'Failed to upload file'}, status=500)

        return Response({'error': 'Invalid request'}, status=400)