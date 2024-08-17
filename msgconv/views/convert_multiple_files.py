
import os
import uuid
import pickle
import logging

from pprint import pformat
from django.conf import settings
from django.shortcuts import render

from msgconv.core.msgconv import msg_extract_info
from msgconv.forms import MultipleFileUploadForm
from msgconv.views.convert_files import MsgConvBase

from sales.common_code import get_readable_file_size

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MsgConvMultipleFiles(MsgConvBase):
    template_name = 'msgconv/msgconv_multiple_files.html'
    
    @method_decorator(login_required)
    def get(self, request, id=None):
        form = MultipleFileUploadForm()
        
        if id:
            # Retrieve the dictionary from disk
            with open(os.path.join(settings.MEDIA_ROOT, id, 'result.pkl'), 'rb') as file:
                result = pickle.load(file)
                
                logger.debug(f'result GET: {pformat(result)}')
                
            return render(request, self.template_name, {'form': form, 'result': result})
        
        return render(request, self.template_name, {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = MultipleFileUploadForm(request.POST, request.FILES)
        return self._process_multiple_files(request, form)
    
    def _process_multiple_files(self, request, form):
        if form.is_valid() and not (form.cleaned_data.get('executed') == 'executed'):
            results = []
            
            # Create folder structure
            self.tmp = str(uuid.uuid4())
            self._create_temp_dirs()
            
            for uploaded_file in request.FILES.getlist('file'):
                # Processing msg file 
                # Write the file to disk
                msg_path = self._write_to_disc(uploaded_file, os.path.join(self.tmp_dir_msg, uploaded_file.name))
                logger.info(f'Uploaded file {uploaded_file.name} size {get_readable_file_size(uploaded_file.size)} directory {self.tmp_dir}')
                
                result = self._process_file(msg_path, uploaded_file)
                result_file_info = msg_extract_info(msg_path)
                result['result_file_info'] = result_file_info
                result['result_file_summaries'] = self._msg_create_summaries(result)
                result['executed'] = 'executed'
                results.append(result)
                logger.debug(f'result: {pformat(results)}')
                
                # Deletes original msg file 
                self._cleanup(msg_path)
            
            # zip all attachments     
            zip_file = self.create_zip_file(self._get_all_file_paths(self.tmp_dir_attachments), 'zip_filename')
            
            return render(request, self.template_name, {'results': results})
        
        return render(request, self.template_name, {'form': form})