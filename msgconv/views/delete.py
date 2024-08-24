import os
import logging
import shutil

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from msgconv.models import Processes
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
            with transaction.atomic():
                # Attempt to get the object first
                try:
                    process = Processes.objects.select_for_update().get(uuid_field=dir_id)
                except ObjectDoesNotExist:
                    logger.warning(f'No database object found for ID {dir_id}')
                    return HttpResponse('Object not found', status=404)

                # Construct the path and check if it exists
                tmp_dir = os.path.join(settings.MEDIA_ROOT, dir_id)
                if os.path.exists(tmp_dir):
                    try:
                        shutil.rmtree(tmp_dir)
                        logger.info(f'Deleted temporary directory {tmp_dir}')
                    except OSError as e:
                        logger.error(f'Error deleting directory {tmp_dir}: {e}')
                        raise
                else:
                    logger.warning(f'No temporary directory found for ID {dir_id}')

                # Delete the database object
                process.delete()
                logger.info(f'Deleted database object for ID {dir_id}')

            return redirect('msgconv_single_files')  # Redirect to a success page

        except Exception as e:
            logger.error(f'Error in delete operation: {e}')
            return HttpResponse('Error during delete operation', status=500)