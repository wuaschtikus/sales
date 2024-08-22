import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete-account.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        logger.info(f'User {user.username} (ID: {user.id}) is deleting their account.')
        response = super().post(request, *args, **kwargs)
        logger.info(f'User {user.username} (ID: {user.id}) has successfully deleted their account.')
        return response

    def delete(self, request, *args, **kwargs):
        """
        Overriding delete to add any custom behavior if needed before deletion.
        """
        user = self.get_object()
        logger.info(f'Preparing to delete user {user.username} (ID: {user.id}).')
        return super().delete(request, *args, **kwargs)
