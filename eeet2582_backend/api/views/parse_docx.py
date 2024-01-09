import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from eeet2582_backend.authentication.authentication import GoogleOAuth2Authentication
from eeet2582_backend.services.parse_docx import ParseDocxService
from eeet2582_backend.celery import app
from eeet2582_backend.services.process_docx import process_user_doc


class ParseDocxAPIView(APIView):
    authentication_classes = [GoogleOAuth2Authentication]

    # permission_classes = []

    @app.task
    def parse_docx_task(file_path, current_user):
        docx_parser = ParseDocxService(file_path, current_user)
        result = docx_parser.parse()
        return result

    def post(self, request, *args, **kwargs):
        if request.FILES.get('docx_file'):
            docx_file = request.FILES['docx_file']

            # TODO: Change this to upload to a temporary directory
            temporary_directory = 'uploads'
            if not os.path.exists(temporary_directory):
                os.makedirs(temporary_directory)

            # TODO: Change this to upload to a temporary directory
            file_path = os.path.join(temporary_directory, docx_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in docx_file.chunks():
                    destination.write(chunk)

            #     result = self.parse_docx_task.delay(file_path).get()
            #
            #     if result:
            #         return Response({"title": result.title}, status=status.HTTP_200_OK)
            #     else:
            #         return Response({"detail": "No title found in the document."}, status=status.HTTP_404_NOT_FOUND)
            #
            # return Response({"detail": "Invalid request. Please provide a DOCX file."}, status=status.HTTP_400_BAD_REQUEST)

            current_user_id = request.user.id

            # result = self.parse_docx_task.delay(file_path, current_user_id)

            result = process_user_doc(file_path, current_user_id)

            return Response({"task_id": result}, status=status.HTTP_202_ACCEPTED)

        return Response({"detail": "Invalid request. Please provide a DOCX file."}, status=status.HTTP_400_BAD_REQUEST)
