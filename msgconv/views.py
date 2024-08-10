import os
import logging
import uuid
import shutil
import pickle
from pprint import pformat

from .forms import SingleFileUploadForm, MultipleFileUploadForm
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse

from .core.msgconv import msg_extract_info, msg_extract_attachments, msg_convert_msg_to_eml_with_signed
from sales.common_code import get_readable_file_size, list_directory

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
    
    
class MsgConvBase(View):
    
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Folder structure
    tmp = str(uuid.uuid4())
    tmp_dir = os.path.join(settings.MEDIA_ROOT, tmp)
    tmp_dir_attachments = os.path.join(tmp_dir, 'attachments')
    tmp_dir_msg = os.path.join(tmp_dir, 'msg')
    tmp_dir_eml = os.path.join(tmp_dir, 'eml')
    tmp_dir_download_eml = os.path.join(settings.MEDIA_URL, tmp, 'eml')
    tmp_dir_download_attachments = os.path.join(settings.MEDIA_URL, tmp, 'attachments')
    tmp_dir_result_path = os.path.join(tmp_dir, 'result.pkl')
    
    def _create_temp_dirs(self):
        os.makedirs(self.tmp_dir_attachments, exist_ok=True)
        os.makedirs(os.path.join(self.tmp_dir, 'msg'), exist_ok=True)
        os.makedirs(self.tmp_dir_eml, exist_ok=True)
        
    def _write_to_disc(self, uploaded_file, save_path):        
        with open(save_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
                
        return save_path
    
    def _cleanup(self, msg_path):
        # Delete the original MSG file if it exists
        if os.path.exists(msg_path):
            os.remove(msg_path)
            logger.info(f'{msg_path} has been deleted successfully.')
        else:
            logger.warning(f'The file {msg_path} does not exist.')
    
    def _process_single_file(self, request, form, uploaded_file):
        if form.is_valid():
            self.uploaded_file = uploaded_file
            self.uploaded_file_size_readable = get_readable_file_size(uploaded_file.size)
            self.uploaded_file_name = uploaded_file.name
            
            # Check file size limit
            if self.uploaded_file.size > self.MAX_UPLOAD_SIZE:
                logger.info('File size exceeded for file ')
                form.add_error(None, f"File size exceeds the 10MB limit. Your file is {self.uploaded_file_size_readable}.")
                return render(request, self.template_name, {'form': form})
            
            # Create folder structure
            self._create_temp_dirs()
                        
            # Processing msg file 
            # Write the file to disk
            msg_path = self._write_to_disc(self.uploaded_file, os.path.join(self.tmp_dir_msg, self.uploaded_file.name))
            logger.info(f'Uploaded file {self.uploaded_file_name} size {self.uploaded_file_size_readable} directory {self.tmp_dir}')

            result = self._process_file(msg_path, uploaded_file)
            result_file_info = msg_extract_info(msg_path)
            result['result_file_info'] = result_file_info
            
            logger.debug(f'result: {pformat(result)}')
            
            # Store result in a file
            # Write the dictionary to disk
            with open(self.tmp_dir_result_path, 'wb') as file:
                pickle.dump(result, file)
            
            self._cleanup(msg_path)
            
            return render(request, self.template_name, {'result': result})
        
        return render(request, self.template_name, {'form': form})
    
    def _process_file(self, msg_path, uploaded_file):
        logger.info(f'File written to disk at {msg_path}')
        
        # Extract attachments (also signed attachments)
        self.attachments_download_path = msg_extract_attachments(msg_path, self.tmp_dir_attachments, self.tmp_dir_download_attachments) 
        self.attachments_download_paths = [d['download_path'] for d in self.attachments_download_path]
        
        # Convert the file to EML format
        eml_path = os.path.join(self.tmp_dir_eml, uploaded_file.name.replace('msg', 'eml'))
        eml_path = self._convert_to_eml(msg_path, eml_path, self.tmp_dir_attachments, self.attachments_download_paths)
        
        logger.info(f'Converted file {msg_path} to EML at {eml_path}')
        
        # Get readable file size
        file_size = get_readable_file_size(uploaded_file.size)
        
        # Generate download URL for the EML file
        eml_filename = os.path.basename(eml_path)
        eml_download_url = os.path.join(self.tmp_dir_download_eml, eml_filename)
        
        return {
            'id': self.tmp,
            'file_name': uploaded_file.name,
            'file_name_download': uploaded_file.name.replace('msg', 'eml'),
            'eml_download_url': eml_download_url,
            'file_size': file_size,
            'attachments_download_paths': self.attachments_download_path,
            'attachments_count': str(len(self.attachments_download_path)),
        }
        
    def _convert_to_eml(self, msg_path, eml_path, msg_attachments_path, attachments):
        eml = msg_convert_msg_to_eml_with_signed(msg_path, eml_path, msg_attachments_path, attachments)
        return eml
        

class MsgConvMultipleFiles(MsgConvBase):
    template_name = 'msgconv/msgconv_multiple_files.html'
    
    def get(self, request, id=None):
        print('get')
        form = MultipleFileUploadForm()
        
        if id:
            # Retrieve the dictionary from disk
            with open(os.path.join(settings.MEDIA_ROOT, id, 'result.pkl'), 'rb') as file:
                result = pickle.load(file)
                
                logger.debug(f'result GET: {pformat(result)}')
                
            return render(request, self.template_name, {'form': form, 'result': result})
        
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        print('post')
        form = MultipleFileUploadForm(request.POST, request.FILES)
        return self._process_multiple_files(request, form)
    
    def _process_multiple_files(self, request, form):
        print(str(request.FILES))
        if form.is_valid():
            results = []
            
            # Create folder structure
            self._create_temp_dirs()
            print('form is valid' + str(request.FILES))
            for uploaded_file in request.FILES.getlist('file'):
                print(uploaded_file)
                # Processing msg file 
                # Write the file to disk
                msg_path = self._write_to_disc(uploaded_file, os.path.join(self.tmp_dir_msg, uploaded_file.name))
                logger.info(f'Uploaded file {uploaded_file.name} size {get_readable_file_size(uploaded_file.size)} directory {self.tmp_dir}')
                
                result = self._process_file(msg_path, uploaded_file)
                print(result)
                result_file_info = msg_extract_info(msg_path)
                print(msg_path)
                print(result_file_info)
                result['result_file_info'] = result_file_info
                results.append(result)
                logger.debug(f'result: {pformat(results)}')
                
                # Store result in a file
                # Write the dictionary to disk
                with open(self.tmp_dir_result_path, 'wb') as file:
                    pickle.dump(result, file)
                    
                self._cleanup(msg_path)
                
                print(str(results))
            
            return render(request, self.template_name, {'results': results})
        
        return render(request, self.template_name, {'form': form})


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
    

class DeleteFiles(View):
    template_name = 'msgconv/delete_files.html'
    
    def get(self, request, id=None):
        file_infos = list_directory(os.path.join(settings.MEDIA_ROOT, id))
        return render(request, self.template_name, {'id': id, 'file_infos': file_infos})

    def post(self, request, id=None):
        file_infos = list_directory(os.path.join(settings.MEDIA_ROOT, id))
        
        if id:
            self._delete(id)
            return redirect('msgconv')
        
        return render(request, self.template_name, {'id': id, 'file_infos': file_infos})
        
        
    def _delete(self, dir_id):
        try:
            tmp_dir = os.path.join(settings.MEDIA_ROOT, dir_id)
            if tmp_dir and os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
                logger.info(f'Deleted temporary directory {tmp_dir}')
            else:
                logger.warning(f'No temporary directory found for ID {self.dir_id}')
            return redirect('msgconv')  # Redirect to a success page
        except Exception as e:
            logger.error(f'Error deleting files: {e}')
            return HttpResponse('Error deleting files', status=500)