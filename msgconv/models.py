from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ConvertedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='converted_files')
    id_value = models.CharField(max_length=255)  # Adjust max_length based on your needs
    result = models.JSONField(default=dict)  # Field to store a dictionary
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.id_value}'