from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

STATUS = (
    (0,"News"),
    (1,"Documents"),
    (2,"Server news"),
    (3,"Final Destination"),
    (4,"Draft"),

)

class Post(models.Model):
    title = models.CharField(max_length = 200, unique = True)
    updated_on = models.DateTimeField(auto_now = True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(choices = STATUS, default = 0)
    image = models.ImageField(default = None, upload_to = 'post_image', blank = True, null = True)
    file = models.FileField(upload_to = "files", blank = True, null = True, default = None)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Music(models.Model):
    name = models.CharField(max_length = 200)
    artist = models.CharField(max_length = 200, blank = True, null = True)
    image = models.ImageField(default = 'music.png', upload_to = 'post_image', blank = True, null = True)
    file = models.FileField(upload_to = "Music", default = None)
    lyrics = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length = 200, blank= True, null= True)
    file = models.FileField(upload_to = "File", default= None)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length = 200, blank= True, null= True)
    image = models.ImageField(upload_to = "Image", default= None)
