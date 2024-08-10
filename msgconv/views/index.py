import logging
from django.shortcuts import render
from django.views import View

# Get an instance of a logger
logger = logging.getLogger(__name__)

class IndexView(View):
    template_name = 'msgconv/index.html'
    def get(self, request):
        return render(request, self.template_name)