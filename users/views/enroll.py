import logging
from django.shortcuts import render
from django.views import View

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Enroll(View):
    template_name = 'base/enroll.html'
    
    def get(self, request):
        period = self.request.GET.get('period', 'monthly')
        return render(request, self.template_name)