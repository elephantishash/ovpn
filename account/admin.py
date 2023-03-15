from django.contrib import admin
from .models import Profile, Server, Account, Action

admin.site.register(Profile)
admin.site.register(Server)
admin.site.register(Account)
admin.site.register(Action)

# Register your models here.
