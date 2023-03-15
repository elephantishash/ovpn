from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Post, Music, Image, File

def home(request):
	context = {}
	try:
		post1 = get_object_or_404(Post, slug='start')
		post2 = get_object_or_404(Post, slug='pin')

		posts = [post1, post2]
		context = {'posts': posts}

	except Exception as e:
		pass
	
	musics = Music.objects.all()[:3]
	context.update({'musics': musics})

	return render(request, 'blog/home.html',context= context)

def profile(request):
	return render(request, 'blog/profile.html')

def files(request, choice):
	print(choice)
	if choice == 'all':
		musics = Music.objects.all()[:3]
		images = Image.objects.all()[:3]
		files = File.objects.all()[:5]

		context = {'images': images, 'musics': musics, 'files': files, 'choice': choice.capitalize()}
	
	elif choice == 'musics':
		musics = Music.objects.all()
		context = {'musics': musics, 'choice': choice.capitalize()}
	
	elif choice == 'images':
		images = Image.objects.all()
		context = {'images': images, 'choice': choice.capitalize()}

	elif choice == 'files':
		files = File.objects.all()
		context = {'files': files, 'choice': choice.capitalize()}
	
	return render(request, 'blog/files.html', context)

def blog(request, choice):
	if choice == 5:
		posts = Post.objects.all().order_by('-created_on')
	else:
		posts = Post.objects.filter(status=choice).order_by('-created_on')

	return render(request, 'blog/blog.html', context={'posts': posts, 'choice': choice})

def post_detail(request, id):
	post = get_object_or_404(Post)
	return render(request, 'blog/post_detail.html', context = {'post': post})




# Create your views here.
