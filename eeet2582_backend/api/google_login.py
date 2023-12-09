import json
import http.client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from eeet2582_backend.models import UserProfile

UserModel = get_user_model()

class GoogleSignIn(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.GET.get('access_token')
        # print(access_token)
        google_account = self.get_google_account(access_token)
        if not google_account:
            return Response({'message': 'Google account not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        print(google_account)
        user = self.get_or_create_user(google_account)

        if user.is_active:
            # Generate JWT token or use any other authentication mechanism
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})

        return Response({'message': 'This account is locked, please contact the admin for more information.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_google_account(self, access_token):
        conn = http.client.HTTPSConnection("www.googleapis.com")
        payload = ''
        headers = {
        'Authorization': access_token
        }
        conn.request("GET", "/oauth2/v1/userinfo?alt=json", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def get_or_create_user(self, google_account):
        try:
            user = UserProfile.objects.get(provider='google', provider_id=google_account['id'])
        except UserProfile.DoesNotExist:
            user = UserProfile.objects.create(
                provider='google',
                provider_id=google_account['id'],
                email=google_account['email'],
                name=google_account['name'],
                picture=google_account['picture'],
            )
        return user
