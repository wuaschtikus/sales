import logging
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


# Get an instance of a logger
logger = logging.getLogger(__name__)

class DeleteAccountView(DeleteView):
    model = User
    template_name = 'users/delete-account.html'
    success_url = reverse_lazy('account_deleted')
    
    def get_object(self, queryset=None):
        return self.request.user