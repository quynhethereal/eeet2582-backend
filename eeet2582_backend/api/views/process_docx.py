import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from eeet2582_backend.services.process_docx import process_latest_docx


class ProcessDocxAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        task_id = process_latest_docx.apply_async()

        return Response({"task_id": task_id.id}, status=status.HTTP_202_ACCEPTED)