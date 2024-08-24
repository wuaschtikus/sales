import uuid
import shutil
import logging 
import os
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin

# Get an instance of a logger
logger = logging.getLogger(__name__)

User = get_user_model()

class ConvertedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='converted_files')
    id_value = models.CharField(max_length=255)  # Adjust max_length based on your needs
    result = models.JSONField(default=dict)  # Field to store a dictionary
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.id_value}'
    
    
admin.site.register(ConvertedFiles)

class Processes(models.Model):
    id = models.AutoField(primary_key=True)
    uuid_field = models.CharField(max_length=36, default=str(uuid.uuid4), editable=False, unique=True)

    def __str__(self):
        return f"{self.id} - {self.uuid_field}"
    
    def delete_directory(self):
        try:
            tmp_dir = os.path.join(settings.MEDIA_ROOT, self.uuid_field)
            if tmp_dir and os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
                logger.info(f'Deleted temporary directory {tmp_dir}')
            else:
                logger.warning(f'No temporary directory found for ID {self.uuid_field}')
        except Exception as e:
            logger.error(f'Error deleting files: {e}')
    
admin.site.register(Processes)
