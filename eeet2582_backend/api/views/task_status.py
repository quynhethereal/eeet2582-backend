from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from eeet2582_backend.authentication.authentication import GoogleOAuth2Authentication
from eeet2582_backend.celery import app


class TaskStatusAPIView(APIView):
    authentication_classes = [GoogleOAuth2Authentication]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')

        if task_id:
            task = app.AsyncResult(task_id)

            if task.state == 'SUCCESS':
                return Response({"task_id": task_id, "result": task.get(), "status": task.state},
                                status=status.HTTP_200_OK)
            elif task.state == 'PENDING':
                return Response({"task_id": task_id, "status": task.state}, status=status.HTTP_202_ACCEPTED)
            elif task.state == 'FAILURE':
                return Response({"task_id": task_id, "status": task.state},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif task.state == 'RETRY':
                return Response({"task_id": task_id, "status": task.state}, status=status.HTTP_200_OK)
            elif task.state == 'STARTED':
                return Response({"task_id": task_id, "status": task.state}, status=status.HTTP_200_OK)
            else:
                return Response({"task_id": task_id, "status": task.state}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid request. Please provide a task ID."},
                            status=status.HTTP_400_BAD_REQUEST)
