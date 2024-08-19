from django.http import HttpResponse
from django.views import View
import os
from django.conf import settings


class AdsTxtView(View):
    def get(self, request, *args, **kwargs):
        with open(os.path.join(settings.STATIC_ROOT, 'ads.txt')) as file:
            file_content = file.readlines()
        return HttpResponse(file_content, content_type="text/plain")
