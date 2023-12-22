from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class Payment(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        test_string = "This is a test response from the Payment API."

        return Response({"message": test_string})