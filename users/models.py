from django.conf import settings
from django.db import models
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class Subscription(models.Model):
    # Define the subscription plan choices
    STARTER = 'starter'
    PRO = 'pro'
    PREMIUM = 'premium'
    
    SUBSCRIPTION_CHOICES = [
        (STARTER, 'Starter'),
        (PRO, 'Pro'),
        (PREMIUM, 'Premium'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default=STARTER)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.get_plan_display()}'
    
    def create_subscription(sender, user):
        Subscription.objects.create(user=user, plan=Subscription.STARTER)
        
    def delete_subscription(self, request):
        subscription = get_object_or_404(Subscription, user=request.user)
        subscription.delete()
        return subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date')