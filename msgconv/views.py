import os
import logging
import uuid
from .core.msgconv import msg_extract_info, msg_extract_attachments, msg_convert_msg_to_eml_with_signed
from .forms import MyFileUploadForm
from django.shortcuts import render
from django.views import View
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)

class IndexView(View):
    template_name = 'msgconv/index.html'
    def get(self, request):
        return render(request, self.template_name)
    
class ConverterView(View):
    template_name = 'msgconv/converter.html'
    def get(self, request):
        return render(request, self.template_name)

class MsgConv(View):
    template_name = 'msgconv/msgconv.html'
    
    def get(self, request):
        form = MyFileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MyFileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # create folder structure
            tmp = str(uuid.uuid4())
            tmp_dir = os.path.join(settings.MEDIA_ROOT, tmp)
            tmp_dir_attachments = os.path.join(tmp_dir, 'attachments')
            tmp_dir_msg = os.path.join(tmp_dir, 'msg')
            tmp_dir_eml = os.path.join(tmp_dir, 'eml')
            tmp_dir_download_eml = os.path.join(settings.MEDIA_URL, tmp, 'eml')
            tmp_dir_download_attachments = os.path.join(settings.MEDIA_URL, tmp, 'attachments')
            os.makedirs(tmp_dir_attachments, exist_ok=True)
            os.makedirs(tmp_dir_msg, exist_ok=True)
            os.makedirs(tmp_dir_eml, exist_ok=True)
            
            uploaded_file = request.FILES['file']
            logger.info(f'Uploaded file {uploaded_file.name}')
            
            # Write the file to disk
            msg_path = self._write_to_disc(uploaded_file, os.path.join(tmp_dir_msg, uploaded_file.name))
            logger.info(f'File {uploaded_file.name} written to disk at {msg_path}')
            
            # Extract attachments (also signed attachments)
            attachments_download_path = msg_extract_attachments(msg_path, tmp_dir_attachments, tmp_dir_download_attachments) 
            attachments_download_paths = [d['download_path'] for d in attachments_download_path]
            
            # Convert the file to EML format
            eml_path = os.path.join(tmp_dir_eml, uploaded_file.name.replace('msg', 'eml'))
            eml_path = self._convert_to_eml(msg_path, eml_path, attachments_download_paths)
            logger.info(f'Converted file {uploaded_file.name} to EML at {eml_path}')
            
            # Get readable file size
            file_size = self._get_readable_file_size(uploaded_file.size)
            
            # Generate download URL for the EML file
            eml_filename = os.path.basename(eml_path)
            eml_download_url = os.path.join(tmp_dir_download_eml, eml_filename)
            
            # Extract summary information from the message
            summary = msg_extract_info(msg_path)
            
            # Delete the original MSG file if it exists
            if os.path.exists(msg_path):
                os.remove(msg_path)
                logger.info(f'{msg_path} has been deleted successfully.')
            else:
                logger.warning(f'The file {msg_path} does not exist.')
            
            # Render the template with the necessary context
            context = {
                'file_name': uploaded_file.name,
                'file_name_download': uploaded_file.name.replace('msg', 'eml'),
                'eml_download_url': eml_download_url,
                'file_size': file_size,
                'attachments_download_paths': attachments_download_path,
                'attachments_count': str(len(attachments_download_path)),
                'summary': summary
            }
            return render(request, self.template_name, context)
        
        return render(request, self.template_name, {'form': form})
    
    def _write_to_disc(self, uploaded_file, save_path):        
        # Write the uploaded file to disk
        with open(save_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
                
        return save_path
    
    def _convert_to_eml(self, msg_path, eml_path, attachments):
        eml = msg_convert_msg_to_eml_with_signed(msg_path, eml_path, attachments)
        # eml = msg_convert_msg_to_eml(msg_path, eml_path)
        return eml
    
    def _get_readable_file_size(self, size_in_bytes):
        size_units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
        size_index = 0

        while size_in_bytes >= 1024 and size_index < len(size_units) - 1:
            size_in_bytes /= 1024
            size_index += 1

        return f"{size_in_bytes:.2f} {size_units[size_index]}"
    
