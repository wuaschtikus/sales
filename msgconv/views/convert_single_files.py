
import os
import pickle
import logging

from pprint import pformat
from django.conf import settings
from django.shortcuts import render

from msgconv.forms import SingleFileUploadForm, MultipleFileUploadForm
from msgconv.views.convert_files import MsgConvBase

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MsgConvSingleFiles(MsgConvBase):
    template_name = 'msgconv/msgconv_single_files.html'
    
    def get(self, request, id=None):
        form = SingleFileUploadForm()
        
        if id:
            # Retrieve the dictionary from disk
            with open(os.path.join(settings.MEDIA_ROOT, id, 'result.pkl'), 'rb') as file:
                result = pickle.load(file)
                logger.debug(f'result GET: {pformat(result)}')
                
            return render(request, self.template_name, {'form': form, 'result': result})
        
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SingleFileUploadForm(request.POST, request.FILES)
        file = request.FILES['file'] 
        return self._process_single_file(request, form, file)
    
    
class MsgConvExcelFiles(MsgConvBase):
    template_name = 'msgconv/msgconv_excel_files.html'
    
    def get(self, request, id=None):
        form = MultipleFileUploadForm()
        return render(request, self.template_name, {'form': form})