from django.conf import settings
from django.shortcuts import redirect 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MY_DOMAIN = settings.FRONT_END_DOMAIN



class StripeCheckoutView(APIView):

    # permission_classes = [IsAuthenticated]    
    def post(self, request):
        try:
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
                mode='subscription',
                success_url=MY_DOMAIN + "/price" + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=MY_DOMAIN + "/price?" + '?canceled=true',
            )
            return Response({'checkout_url':checkout_session.url} , 200)
        except Exception as e:
            print(e)
            return Response(
                {'error': "Invalid Checkout."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )