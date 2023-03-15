from django.contrib import admin
from .models import Post, Music, File, Image

admin.site.register(Post)
admin.site.register(Music)
admin.site.register(File)
admin.site.register(Image)