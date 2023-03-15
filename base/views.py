from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from blog.models import Post, Music, Image, File


def home(request):
	return render(request, 'base/home.html')

# Create your views here.
