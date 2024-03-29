from django.conf import settings
from django.shortcuts import redirect 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.user_model import User
from ..models.payment_model import Payment  
from django.views.decorators.csrf import csrf_exempt

import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MY_DOMAIN = settings.FRONT_END_DOMAIN



class StripeCheckoutView(APIView):

    permission_classes = [IsAuthenticated]    
    def post(self, request):

        user = request.user
        payment = Payment.objects.filter(user=user).first()

        try:
            # Retrieve the new price based on the lookup_key
            prices = stripe.Price.list(
                lookup_keys=[request.data.get('lookup_key')],
                expand=['data.product']
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                customer = payment.stripe_customer_id,
                mode='subscription',
                success_url=MY_DOMAIN + "price" + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=MY_DOMAIN + "price" + '?canceled=true',
            )
            return Response({'checkout_url':checkout_session.url} , 200)
        except Exception as e:
            print(e)
            return Response(
                {'error': "Invalid Checkout."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def get(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Query the Payment model for the user's payment data
            payment = Payment.objects.filter(user=user).first()

            if payment:
                # Serialize the payment data to send as a response
                
                payment_data = {
                    'plan_name': payment.plan_name,
                     'price' : payment.price,
                    'status': payment.status,
                    'end_date': payment.end_date,
                }
                return Response(payment_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No payment information found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response(
                {'error': "Error fetching payment information."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Query the Payment model for the user's payment data
            payment = Payment.objects.filter(user=user).first()

            if payment and payment.stripe_customer_id:
                # Get the current active and trialing plans
                active_subscriptions = stripe.Subscription.list(customer=payment.stripe_customer_id, status='active')
                trialing_subscriptions = stripe.Subscription.list(customer=payment.stripe_customer_id, status='trialing')

                # Cancel active subscriptions at the period's end
                for subscription in active_subscriptions.auto_paging_iter():
                    stripe.Subscription.modify(subscription.id, cancel_at_period_end=True)

                # Immediately cancel trialing subscriptions
                for subscription in trialing_subscriptions.auto_paging_iter():
                    stripe.Subscription.modify(subscription.id, cancel_at_period_end=True)

                return Response({"message": "Subscription(s) cancelled successfully. Access continues until the end of the billing period for active plans."}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'No active or trialing subscription found for user.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f"Error updating subscription: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

