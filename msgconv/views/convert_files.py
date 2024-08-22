
import os
import uuid
import pickle
import logging
import json
import csv
import pprint
import zipfile

from datetime import datetime
from pprint import pformat
from django.conf import settings
from django.shortcuts import render
from django.views import View

from msgconv.core.msgconv import msg_extract_info, msg_extract_attachments, msg_convert_msg_to_eml_with_signed
from msgconv.forms import SingleFileUploadForm, MultipleFileUploadForm
from sales.common_code import get_readable_file_size

logger = logging.getLogger(__name__)

class MsgConvBase(View):
    
    def _create_temp_dirs(self):
        self.tmp = str(uuid.uuid4())
        self.tmp_dir = os.path.join(settings.MEDIA_ROOT, self.tmp)
        self.tmp_dir_attachments = os.path.join(self.tmp_dir, 'attachments')
        self.tmp_dir_msg = os.path.join(self.tmp_dir, 'msg')
        self.tmp_dir_eml = os.path.join(self.tmp_dir, 'eml')
        self.tmp_dir_download_eml = os.path.join(settings.MEDIA_URL, self.tmp, 'eml')
        self.tmp_dir_download_attachments = os.path.join(settings.MEDIA_URL, self.tmp, 'attachments')
        self.tmp_dir_result_path_pkl = os.path.join(self.tmp_dir, 'result.pkl')
        self.tmp_dir_result_path_txt = os.path.join(self.tmp_dir, 'result.txt')
        self.tmp_dir_result_path_csv = os.path.join(self.tmp_dir, 'result.csv')
        self.tmp_dir_result_path_json = os.path.join(self.tmp_dir, 'result.json')
        
        os.makedirs(self.tmp_dir_attachments, exist_ok=True)
        os.makedirs(os.path.join(self.tmp_dir, 'msg'), exist_ok=True)
        os.makedirs(self.tmp_dir_eml, exist_ok=True)
        
    def _get_current_datetime_for_filename(self):
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string suitable for a filename
        formatted_datetime = now.strftime("%Y%m%d_%H%M%S")
        formatted_datetime = f'{formatted_datetime}'
        return formatted_datetime
        
    def _create_zip_file(self, zip_filename):
        # zip all attachments
        files = self._get_all_file_paths(os.path.join(settings.BASE_DIR, 'media', self.tmp, 'attachments'))
        
        logger.debug('produced zip file')
        
        # Define the full path where the ZIP file will be saved
        zip_file_path = f"{zip_filename}"
        
        # Open the ZIP file in write mode on disk
        with zipfile.ZipFile(zip_file_path, 'w') as zf:
            for file_path in files:
                # Get the file name from the path
                file_name = os.path.basename(file_path)
                # Write the file to the ZIP archive
                zf.write(file_path, file_name)
        
        # Return the path to the saved ZIP file
        return zip_file_path
    
    def _get_all_file_paths(self, directory):
        file_paths = []
        # Walk through the directory
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Create the full filepath by joining the root and filename
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths
        
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
        logger.debug('recieved post request')
        #logger.debug(f'recieved form {form}')
        
        # prevent spamming reload page, fill text field with 'executed'
        # when file was processed
        # field gets reset on client if the user chooses another file
        if form.is_valid() and not (form.cleaned_data.get('executed') == 'executed'): 
            logger.debug('form is valid and field executed was does not contain executed flag')
            self.uploaded_file = form.cleaned_data['file']
            self.uploaded_file = uploaded_file
            self.uploaded_file_size_readable = get_readable_file_size(uploaded_file.size)
            self.uploaded_file_name = uploaded_file.name
            
            # Create folder structure
            # Generate a new directory id 
            self.tmp = str(uuid.uuid4())
            self._create_temp_dirs()
                        
            # Processing msg file 
            # Write the file to disk
            msg_path = self._write_to_disc(self.uploaded_file, os.path.join(self.tmp_dir_msg, self.uploaded_file.name))
            logger.info(f'Uploaded file {self.uploaded_file_name} size {self.uploaded_file_size_readable} directory {self.tmp_dir}')

            result = self._process_file(msg_path, uploaded_file)
            result['result_file_info'] = msg_extract_info(msg_path)
            result['result_file_summaries'] = self._msg_create_summaries(result)
            result['executed'] = 'executed'
            
            #logger.debug(f'result: {pformat(result)}')
            
            self._cleanup(msg_path)
            
            return render(request, self.template_name, {'result': result})
        logger.debug(f'Form errors: {form.errors}' )
        logger.debug('Form is not valid')
        return render(request, self.template_name, {'form': form})
    
    def _msg_create_summaries(self, result):
        # Store result in a file
        # Write the dictionary to disk
        with open(self.tmp_dir_result_path_pkl, 'wb') as file:
            pickle.dump(result, file)
            
        # Write the dictionary to a text file
        with open(self.tmp_dir_result_path_txt, 'w', encoding='utf-8') as file:
            file.write(pprint.pformat(result, indent=4))
            
        # Write the dictionary to a JSON file
        with open(self.tmp_dir_result_path_json, 'w',  encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            
        # Write the dictionary to a CSV file
        with open(self.tmp_dir_result_path_csv, 'w', newline='',  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(result.keys())
            writer.writerow(result.values())
            
        return {
            'txt': os.path.join(settings.MEDIA_URL, self.tmp, 'result.txt'),
            'json': os.path.join(settings.MEDIA_URL, self.tmp, 'result.json'),
            'csv': os.path.join(settings.MEDIA_URL, self.tmp, 'result.csv')
        }
        
    
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