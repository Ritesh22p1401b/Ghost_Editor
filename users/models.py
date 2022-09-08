import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime 
from django.utils import timezone   

class ExtendUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"   
    EMAIL_FIELD = "email"       

class Author(models.Model):
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reference_id=models.UUIDField(default=uuid.uuid4)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=240, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    description = models.CharField(max_length=150, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

