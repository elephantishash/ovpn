from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from account.models import Profile, Account, Action, Server
from django.core.files import File
from django.utils import timezone
import datetime
import os

def home(request):
	profiles = Profile.objects.all()
	servers = Server.objects.all()

	context = {'profiles': profiles,
		'servers': servers,
	}
	return render(request, 'superadmin/home.html', context = context)

def profile(request, profile):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profile = get_object_or_404(Profile, id=profile)
			accounts = Account.objects.filter(leader=profile).order_by('-created_on')
			accounts_count = accounts.count()
			all_account = profile.count
			accounts_left = all_account - accounts_count

			servers = Server.objects.all()

			today = timezone.datetime.today().day

			context = {'profile': profile,
				'accounts': accounts,
				'accounts_count': accounts_count,
				'accounts_left': accounts_left,
				'today': today,
				'servers': servers,
			} 

			return render(request, 'superadmin/profile.html', context)
	else:
		return redirect('account:login_view')

def change_server(request, profile_id):
	profile = get_object_or_404(Profile, id=profile_id)
	server = get_object_or_404(Server, name=request.POST['server_shift'])
	profile.server = server
	profile.save()
	return redirect('superadmin:profile', profile_id)


def server(request, server_id):
	server = get_object_or_404(Server, id=server_id)
	profiles = Profile.objects.filter(server=server)
	context = {
		'server': server,
		'profiles': profiles,
	}
	return render(request, 'superadmin/server.html', context)




