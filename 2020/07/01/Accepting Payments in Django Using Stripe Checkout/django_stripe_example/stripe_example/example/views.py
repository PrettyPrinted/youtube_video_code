from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def index(request):
    return render(request, 'index.html')

def thanks(request):
    return render(request, 'thanks.html')

@csrf_exempt
def checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1H06q8IdX0gthvYPWudV1aw1',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('index')),
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })

@csrf_exempt
def stripe_webhook(request):

    print('WEBHOOK!')
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = 'whsec_Xj8wBk2qiUcjDEmYu5kfKkOrJCJ5UUjW'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=200)