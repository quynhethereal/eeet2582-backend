import datetime
from django.conf import settings
from ..models.user_model import User
from ..models.payment_model import Payment  
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe


@csrf_exempt  # CSRF protection is not needed for this view
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the specific webhook events

    if event['type'] == 'customer.subscription.created':
        print("create subscription")
        # Handle subscription creation
        data = event['data']['object']
        # # Retrieve or create the Payment record
        subscription = stripe.Subscription.retrieve(data.stripe_id)
        subscription_data = subscription.to_dict()
        print(subscription)
        payment, created = Payment.objects.get_or_create(
            stripe_subscription_id=subscription.id
        )
        payment.plan_name = subscription_data['items']['data'][0]['price']['lookup_key']
        payment.price =  subscription_data['items']['data'][0]['plan']['amount'] / 100
        
        payment.status = subscription.status
        payment.start_date = datetime.fromtimestamp(subscription.current_period_start)
        payment.end_date = datetime.fromtimestamp(subscription.current_period_end)
        payment.save()

    elif event['type'] == 'customer.subscription.updated':
        print(" subscription update")
        pass
    elif event['type'] == 'customer.subscription.deleted':
        print("delete")
        pass
    elif event['type'] == 'invoice.created' or event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # Check if this is the end of the trial period
        if subscription['trial_end'] and subscription['metadata'].get('cancel_after_trial') == 'true':
            try:
                stripe.Subscription.delete(subscription['id'])
                
            except stripe.error.StripeError as e:
                # Handle error
                print(e)

    return HttpResponse(status=200)