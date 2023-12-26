from ..models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import http.client
import json


class GoogleSignIn(APIView):
    def post(self, request, *args, **kwargs):
        # Extracting the access token from the Authorization header
        access_token = self.extract_access_token(request)

        if not access_token:
            return Response({'message': 'Access token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        google_account = self.get_google_account(access_token)
        if not google_account:
            return Response({'message': 'Google account not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user data from Google account
        id = google_account.get('id')

        email = google_account.get('email')
        print(type(email))

        # Check if the user exists in the database or create a new one
        user, created = User.objects.update_or_create(
            id=id,
            email=email,
        )

        return Response({'message': 'Login success.', 'user_id': user.pk}, status=status.HTTP_200_OK)

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
