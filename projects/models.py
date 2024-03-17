from django.db import models
import os
from django.utils.text import slugify
from django.utils import timezone

def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]  # Get the filename extension
    slug = slugify(instance.title)  # Generate a slug from the project title
    new_filename = f'{slug}.{ext}'
    return os.path.join('brand_logo', slug, new_filename)

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand_logo = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

    def __str__(self):
        return self.title

