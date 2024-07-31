from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import MyForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ViewUserProfile(LoginRequiredMixin, FormView):
    template_name = 'account/profile.html'  # Template to render the form
    form_class = MyForm
    success_url = reverse_lazy('form_success')  # URL to redirect after successful form submission

    def get_initial(self):
        initial = super().get_initial()
        # Prepopulate the email field with the user's email
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        # Process the data in form.cleaned_data as required
        # For example, send an email or save to database
        print(form.cleaned_data)
        return super().form_valid(form)