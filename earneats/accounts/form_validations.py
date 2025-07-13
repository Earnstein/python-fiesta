from django.core.exceptions import ValidationError
from os import path

def allow_images_only(value):
    ext = path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')