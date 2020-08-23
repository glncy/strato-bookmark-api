from django.db import models

# Create your models here.

class Bookmark(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000, blank=True, default='')
    url = models.TextField()
    tags = models.TextField(default='')

class Tags(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000, blank=True, default='')