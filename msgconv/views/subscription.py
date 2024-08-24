import logging
import stripe
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy

from django.conf import settings
import os
# Get an instance of a logger
logger = logging.getLogger(__name__)

class Subscription(View):
    template_name = 'msgconv/subscription.html'
    def get(self, request):
        
        session = stripe.checkout.Session.create(
            success_url=os.path.join(reverse_lazy('subscription_success'), self.request.user.get_session_auth_hash())
        )
                    
        context = {
            'STRIPE_PAYMENT_URL_STARTER_MONTHLY': settings.STRIPE_PAYMENT_URL_STARTER_MONTHLY,
            'STRIPE_PAYMENT_URL_PREMIUM_MONTHLY': settings.STRIPE_PAYMENT_URL_PREMIUM_MONTHLY,
            'STRIPE_PAYMENT_URL_PRO_MONTHLY': settings.STRIPE_PAYMENT_URL_PRO_MONTHLY,
            'STRIPE_PAYMENT_CUSTOMER_PORTAL': settings.STRIPE_PAYMENT_CUSTOMER_PORTAL
        }
        return render(request, self.template_name, context)