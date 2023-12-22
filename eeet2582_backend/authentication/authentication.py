from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import requests
from ..api.models.user_model import User  # Ensure you import your User model

class GoogleOAuth2Authentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None

        access_token = authorization_header.split(' ')[1]
        user_info = self.get_google_user_info(access_token)

        if user_info is None:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Use the custom user model's manager to get or create a user
        user = self.get_or_create_user(user_info)

        return (user, None)  # authentication successful

    def get_google_user_info(self, access_token):
        """
        Validate an access token against Google OAuth and return the user info.
        """
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'access_token': access_token}
        )

        if response.status_code != 200:
            return None

        return response.json()

    def get_or_create_user(self, user_info):
        """
        Get or create a user based on Google user info.
        """
        user_id = user_info.get('sub')  # Google's unique ID for the user
        email = user_info.get('email')

        # Ensure that user_id and email are present
        if not user_id or not email:
            raise exceptions.AuthenticationFailed('Missing Acco ID or email')

        user, created = User.objects.get_or_create(
            id=user_id,
            defaults={'email': email}
        )

        # If user already exists, update email if it's different
        if not created and user.email != email:
            user.email = email
            user.save()

        return user
