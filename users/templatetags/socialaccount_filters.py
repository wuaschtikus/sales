# myapp/templatetags/socialaccount_filters.py

from django import template
from allauth.socialaccount.models import SocialAccount

register = template.Library()
print('loaded')
@register.filter
def is_connected(user, provider_id):
    return SocialAccount.objects.filter(user=user, provider=provider_id).exists()
