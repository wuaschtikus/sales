from django.urls import reverse_lazy
from django.views.generic import TemplateView
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount


class ProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get the primary email for the user
        try:
            email_address = EmailAddress.objects.get(user=user, primary=True)
            context['email_verified'] = email_address.verified
            
            has_social_account = SocialAccount.objects.filter(user=user).exists()
            context['has_social_account'] = has_social_account
        except EmailAddress.DoesNotExist:
            context['email_verified'] = False  
        
        return context