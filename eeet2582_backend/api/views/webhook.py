from django.utils import timezone
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

        # Delete any existing trial subscriptions
        for sub in stripe.Subscription.list(customer=subscription.customer):
            if sub.id != subscription.id and sub.status == 'trialing':
                stripe.Subscription.delete(sub.id)
                
        #update payment info
        payment = Payment.objects.get(
            stripe_customer_id = subscription.customer
        )
        payment.plan_name = subscription_data['items']['data'][0]['price']['lookup_key']
        payment.price =  subscription_data['items']['data'][0]['plan']['amount'] / 100
        
        payment.status = subscription.status
        payment.start_date = timezone.make_aware(timezone.datetime.fromtimestamp(subscription.current_period_start))
        payment.end_date = timezone.make_aware(timezone.datetime.fromtimestamp(subscription.current_period_end))
        payment.save()

    elif event['type'] == 'customer.subscription.updated':
        print(" subscription update")
        data = event['data']['object']
        subscription = stripe.Subscription.retrieve(data.stripe_id)
        
        if subscription.cancel_at_period_end == False:
            pass

        
        #update payment info
        payment = Payment.objects.get(
            stripe_customer_id = subscription.customer
        )
        
        payment.status = "endsoon"
        payment.save()
        
    elif event['type'] == 'customer.subscription.deleted':
        print("delete")
        pass

    return HttpResponse(status=200)