import os
import logging
import shutil

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from sales.common_code import list_directory

# Get an instance of a logger
logger = logging.getLogger(__name__)

class DeleteFiles(View):
    template_name = 'msgconv/delete_files.html'
    
    def get(self, request, id=None):
        file_infos = list_directory(os.path.join(settings.MEDIA_ROOT, id))
        return render(request, self.template_name, {'id': id, 'file_infos': file_infos})

    def post(self, request, id=None):
        file_infos = list_directory(os.path.join(settings.MEDIA_ROOT, id))
        
        if id:
            self._delete(id)
            return redirect('msgconv_single_files')
        
        return render(request, self.template_name, {'id': id, 'file_infos': file_infos})
        
    def _delete(self, dir_id):
        try:
            tmp_dir = os.path.join(settings.MEDIA_ROOT, dir_id)
            if tmp_dir and os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
                logger.info(f'Deleted temporary directory {tmp_dir}')
            else:
                logger.warning(f'No temporary directory found for ID {dir_id}')
            return redirect('msgconv_single_files')  # Redirect to a success page
        except Exception as e:
            logger.error(f'Error deleting files: {e}')
            return HttpResponse('Error deleting files', status=500)