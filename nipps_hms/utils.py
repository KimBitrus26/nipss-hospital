from uuid import uuid4
from django.core.exceptions import ValidationError
import os

def generate_slug_code():
    
    return uuid4()


def validate_file(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only pdf, jpg, png and jpeg are supported')

    if value.size > 1048576*2:
        raise ValidationError("The maximum file size is 2MB")

    return value