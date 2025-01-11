# models.py
from django.db import models
from django.core.validators import FileExtensionValidator

class UploadedFile(models.Model):
    file = models.FileField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"File uploaded at {self.uploaded_at}"

