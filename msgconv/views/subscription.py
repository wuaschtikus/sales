import logging
from django.shortcuts import render
from django.views import View
from django.conf import settings
# Get an instance of a logger
logger = logging.getLogger(__name__)

class Subscription(View):
    template_name = 'msgconv/subscription.html'
    def get(self, request):
        context = {
            'STRIPE_PAYMENT_URL_STARTER_MONTHLY': settings.STRIPE_PAYMENT_URL_STARTER_MONTHLY,
            'STRIPE_PAYMENT_URL_PREMIUM_MONTHLY': settings.STRIPE_PAYMENT_URL_PREMIUM_MONTHLY,
            'STRIPE_PAYMENT_URL_PRO_MONTHLY': settings.STRIPE_PAYMENT_URL_PRO_MONTHLY,
        }
        return render(request, self.template_name, context)