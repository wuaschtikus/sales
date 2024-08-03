import os
from .core.msgconv import convert_msg_to_eml
from django.views.generic import ListView, DetailView, FormView
from .forms import MyFileUploadForm
from django.shortcuts import render
from django.views import View
from django.conf import settings

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
            # Process the file here
            uploaded_file = request.FILES['file']
            msg_path = self._write_to_disc(uploaded_file)
            eml_path = os.path.join(settings.MEDIA_ROOT, 'eml_files', uploaded_file.name.replace('msg', 'eml'))
            eml_path = self._convert_to_eml(msg_path, eml_path)
            file_size = self._get_readable_file_size(uploaded_file.size)
            
            # Generate the download URL for the EML file
            eml_filename = os.path.basename(eml_path)
            eml_download_url = os.path.join(settings.MEDIA_URL, 'eml_files', eml_filename)
                        
            # Render and provide download link 
            return render(request, self.template_name, {
                'file_name': uploaded_file.name,
                'file_name_download': uploaded_file.name.replace('msg', 'eml'),
                'eml_download_url': eml_download_url,
                'file_size': file_size
            })
        return render(request, self.template_name, {'form': form})
    
    def _write_to_disc(self, uploaded_file):
        save_path = os.path.join(settings.MEDIA_ROOT, 'msg_files', uploaded_file.name)
        
        # Write the uploaded file to disk
        with open(save_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
                
        return save_path
    
    def _convert_to_eml(self, msg_path, eml_path):
        eml = convert_msg_to_eml(msg_path, eml_path)
        
        return eml
    
    def _get_readable_file_size(self, size_in_bytes):
        # Define the size units in order
        size_units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
        size_index = 0  # Starting with Bytes

        # Convert size to the appropriate unit
        while size_in_bytes >= 1024 and size_index < len(size_units) - 1:
            size_in_bytes /= 1024
            size_index += 1

        # Return the size and the unit
        return f"{size_in_bytes:.2f} {size_units[size_index]}"
