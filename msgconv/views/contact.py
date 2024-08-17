
import logging
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from msgconv.forms import ContactForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('index')  # Redirect after successful form submission

    def form_valid(self, form):
         # Get the cleaned data from the form
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # Create the email content
        subject = f"New Contact Form Submission from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['martin.midori@gmail.com']

        # Send the email
        send_mail(subject, message_body, from_email, recipient_list)

        return super().form_valid(form)