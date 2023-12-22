import json
import http.client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class GoogleSignIn(APIView):
    def post(self, request, *args, **kwargs):
        # Extracting the access token from the Authorization header
        access_token = self.extract_access_token(request)

        if not access_token:
            return Response({'message': 'Access token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        print(access_token)

        google_account = self.get_google_account(access_token)
        if not google_account:
            return Response({'message': 'Google account not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        print(google_account)
        # Should check if the user exists in the database or create a new one

        return Response({'message': 'Login success.'}, status=status.HTTP_200_OK)

    def extract_access_token(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            return authorization_header.split(' ')[1]
        return None

    def get_google_account(self, access_token):
        conn = http.client.HTTPSConnection("www.googleapis.com")
        payload = ''
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        conn.request("GET", "/oauth2/v1/userinfo?alt=json", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
