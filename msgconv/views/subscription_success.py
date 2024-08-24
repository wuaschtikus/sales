import logging
import stripe
from django.shortcuts import render
from django.views import View
from django.conf import settings
# Get an instance of a logger
logger = logging.getLogger(__name__)

class SubscriptionSuccess(View):
    template_name = 'msgconv/subscription_success.html'
    def get(self, request):
        
        return render(request, self.template_name)