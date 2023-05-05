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

current_dir = os.getcwd()

def account_generator(profile, server, account_name):
	server_ip = server.ir_ip
	for i in os.listdir('{}/cli/{}'.format(current_dir, server_ip)):
		if i.startswith('cli_'):
			none_name = i
			break

	global pas
	pas = ''
	with open('{}/cli/{}/pass.txt'.format(current_dir, server_ip), 'r') as f:
		lines = f.readlines()
		for line in lines:
			print(line)
			if line.startswith(none_name):
				pas = line.split(' : ')[1]

	os.rename('{}/cli/{}/{}'.format(current_dir, server_ip, none_name), '{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name))
	with open('{}/cli/{}/{}.ovpn'.format(current_dir,server_ip, account_name), 'rb') as f:
		ovpn_file = File(f)
		ovpn_file = File(f, name=os.path.basename('{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name)))
		account = Account(name=account_name, password = pas, file = ovpn_file, server = server, cli_name = none_name.split('.')[0], leader = profile)
		account.save()

	action = Action(leader = profile, action = 0, account = account)
	action.save()

def home(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profiles = Profile.objects.all()
			servers = Server.objects.all()
			accounts = Account.objects.all()

			admin_accounts = Account.objects.filter(leader=get_object_or_404(Profile, user=request.user)).order_by('-date_end')

			context = { 'profiles': profiles,
				'servers': servers,
				'accounts': accounts,
				'admin_accounts': admin_accounts,
			}


			return render(request, 'superadmin/home.html', context=context)
	else:
		return redirect('account:login_view')

def manage(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profiles = Profile.objects.all()
			servers = Server.objects.all()

			context = {'profiles': profiles,
				'servers': servers,
			}
			return render(request, 'superadmin/manage.html', context = context)
	else:
		return redirect('account:login_view')

def profile(request, profile):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profile = get_object_or_404(Profile, id=profile)
			accounts = Account.objects.filter(leader=profile).order_by('-date_end')
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
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profile = get_object_or_404(Profile, id=profile_id)
			server = get_object_or_404(Server, name=request.POST['server_shift'])
			profile.server = server
			profile.save()
			return redirect('superadmin:profile', profile_id)
	else:
		return redirect('account:login_view')


def server(request, server_id):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			server = get_object_or_404(Server, id=server_id)
			profiles = Profile.objects.filter(server=server)
			context = {
				'server': server,
				'profiles': profiles,
			}
			return render(request, 'superadmin/server.html', context)
	else:
		return redirect('account:login_view')

def create_account(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			account_name = request.POST['account_name']
			server = get_object_or_404(Server, name=request.POST['server_shift'])
			profile = get_object_or_404(Profile, user=request.user)

			account_generator(profile, server, account_name)
			print('i am here biiiiiitch')

			return redirect('superadmin:home')

	else:
		return redirect('account:login_view')



