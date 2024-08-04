import os
import logging
from .core.msgconv import msg_extract_info, msg_convert_msg_to_eml, msg_extract_attachments
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
            uploaded_file = request.FILES['file']
            logger.info(f'Uploaded file {uploaded_file.name}')
            
            # Write the file to disk
            msg_path = self._write_to_disc(uploaded_file)
            logger.info(f'File {uploaded_file.name} written to disk at {msg_path}')
            
            # Convert the file to EML format
            eml_path = os.path.join(settings.EML_FILES_DIR, uploaded_file.name.replace('msg', 'eml'))
            eml_path = self._convert_to_eml(msg_path, eml_path)
            logger.info(f'Converted file {uploaded_file.name} to EML at {eml_path}')
            
            # Get readable file size
            file_size = self._get_readable_file_size(uploaded_file.size)
            
            # Extract attachments
            attachments_download_path = msg_extract_attachments(msg_path, settings.MSG_ATTACHMENTS_DIR, settings.MSG_ATTACHMENTS_DIR)
            print('Attachments: ' + str(attachments_download_path))
                        
            # Generate download URL for the EML file
            eml_filename = os.path.basename(eml_path)
            eml_download_url = os.path.join(settings.EML_FILES_DIR, eml_filename)
            
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
                'summary': summary
            }
            return render(request, self.template_name, context)
        
        return render(request, self.template_name, {'form': form})
    
    def _write_to_disc(self, uploaded_file):
        save_path = os.path.join(settings.MSG_FILES_DIR, uploaded_file.name)
        
        # Write the uploaded file to disk
        with open(save_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
                
        return save_path
    
    def _convert_to_eml(self, msg_path, eml_path):
        eml = msg_convert_msg_to_eml(msg_path, eml_path)
        return eml
    
    def _get_readable_file_size(self, size_in_bytes):
        size_units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
        size_index = 0

        while size_in_bytes >= 1024 and size_index < len(size_units) - 1:
            size_in_bytes /= 1024
            size_index += 1

        return f"{size_in_bytes:.2f} {size_units[size_index]}"