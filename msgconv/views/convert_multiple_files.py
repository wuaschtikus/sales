
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
            
            zip = self._zip_attachments()
            zip_file = {
                'result_zip_file_download_link': zip,
                'result_zip_file_name': os.path.basename(zip)
            }
                        
            for uploaded_file in request.FILES.getlist('file'):
                # Processing msg file 
                # Write the file to disk
                msg_path = self._write_to_disc(uploaded_file, os.path.join(self.tmp_dir_msg, uploaded_file.name))
                logger.info(f'Uploaded file {uploaded_file.name} size {get_readable_file_size(uploaded_file.size)} directory {self.tmp_dir}')
                
                result = {}
                result = self._process_file(msg_path, uploaded_file)
                result_file_info = msg_extract_info(msg_path)
                result['result_file_info'] = result_file_info
                result['result_file_summaries'] = self._msg_create_summaries(result)
                result['executed'] = 'executed'
                results.append(result)
                logger.debug(f'result: {pformat(results)}')
                
                # Deletes original msg file 
                self._cleanup(msg_path)
            
            return render(request, self.template_name, {'results': results, 'zip': zip_file})
        
        return render(request, self.template_name, {'form': form})
    
    def _zip_attachments(self):
        zip_file_name = self._get_current_datetime_for_filename()    
        zip_file_path = os.path.join(settings.BASE_DIR, 'media', self.tmp, 'attachments', f'{zip_file_name}.zip')
        zip_file = self._create_zip_file(zip_file_path)
        zip_download_link = os.path.join(self.tmp_dir_download_attachments, f'{zip_file_name}.zip')
        
        logger.debug(f'zip download link: {zip_file}')
        
        return zip_download_link