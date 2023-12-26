from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import requests
import stripe
from django.utils import timezone
from django.conf import settings
from ..api.models.user_model import User  # Ensure you import your User model
from ..api.models.payment_model import Payment

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

               
        if created: # Assign a Stripe subscription with a trial period on first login
            self.create_stripe_subscription(user)

        return user
    

    def create_stripe_subscription(self, user):
        try:
            # Create a Stripe Customer
            customer = stripe.Customer.create(email=user.email)

            # Assign the customer to a subscription plan with a 20-day trial
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'price': settings.STRIPE_3MONTH_PRICE_ID}],  # Replace with your Stripe plan ID
                trial_period_days=20,
                trial_settings={"end_behavior": {"missing_payment_method": "cancel"}},
            )


            # Create or update the Payment record
            subscription_data = subscription.to_dict()
            payment, created = Payment.objects.update_or_create(
                user=user,
                defaults={
                    'stripe_subscription_id': subscription.id,
                    'stripe_customer_id': customer.id,
                    'plan_name':subscription_data['items']['data'][0]['price']['lookup_key'], 
                    'status': subscription.status,
                    'start_date': timezone.make_aware(timezone.datetime.fromtimestamp(subscription.current_period_start)),
                    'end_date': timezone.make_aware(timezone.datetime.fromtimestamp(subscription.current_period_end)),
                    'price': subscription_data['items']['data'][0]['plan']['amount'] / 100
                }
            )           

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")