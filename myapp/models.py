from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    blog_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'posts'
        
    # delete old image
    def save(self, *args, **kwargs):
        try:
            old_instance = Post.objects.get(pk=self.pk)
            old_image = old_instance.blog_image
            if old_image and old_image != self.blog_image:
                if default_storage.exists(old_image.name):
                    default_storage.delete(old_image.name)
        except Post.DoesNotExist:
            pass
        super().save(*args, **kwargs)
