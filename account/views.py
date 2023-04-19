from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Profile, Account, Action, Server
from django.core.files import File
from django.utils import timezone
import datetime
import os

def profile(request):
	if request.user.is_authenticated:

		profile = get_object_or_404(Profile, user = request.user)
		accounts = Account.objects.filter(leader=profile).order_by('-created_on')
		accounts_count = accounts.count()
		all_account = profile.count
		accounts_left = all_account - accounts_count

		today = timezone.datetime.today().day

		context = {'profile': profile,
			'accounts': accounts,
			'accounts_count': accounts_count,
			'accounts_left': accounts_left,
			'today': today,
		} 

		return render(request, 'account/profile.html', context)
	else:
		return redirect('account:login_view')

def check(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('account:profile')
		else:
			messages.add_message(request, messages.INFO, 'Bad Username/Password')
			return redirect('account:login_view')

def login_view(request):
	return render(request, 'account/login.html')

def create_account(request):
	if request.user.is_authenticated:
		account_name = request.POST['account_name']

		if account_name != "":
			if get_object_or_404(Account, name=account_name):
				messages.add_message(request, messages.INFO, 'This name already taken')
			else:
				profile = get_object_or_404(Profile, user = request.user)
				server_ip = profile.server.ir_ip
				

				for i in os.listdir('cli/{}'.format(server_ip)):
					if i.startswith('cli_'):
						none_name = i
						break

				global pas
				pas = ''
				with open('cli/{}/pass.txt'.format(server_ip), 'r') as f:
					lines = f.readlines()
					for line in lines:
						print(line)
						if line.startswith(none_name):
							pas = line.split(' : ')[1]

				os.rename('cli/{}/{}'.format(server_ip, none_name), 'cli/{}/{}.ovpn'.format(server_ip, account_name))
				with open('cli/{}/{}.ovpn'.format(server_ip, account_name), 'rb') as f:
					ovpn_file = File(f)	
					account = Account(name=account_name, password = pas, file = ovpn_file, server = profile.server, cli_name = none_name.split('.')[0], leader = profile)
					account.save()

				action = Action(leader = get_object_or_404(Profile, user = request.user), action = 0, account = account)
				action.save()
		else:
			messages.add_message(request, messages.INFO, 'Bad Username! donnot creat none name account')

		return redirect('account:profile')
	else:
		return redirect('account:profile')

def charge_account(request, account_id):
	if request.user.is_authenticated:
		account = get_object_or_404(Account, id=account_id)
		account.date_end += datetime.timedelta(days=30)
		account.save()

		leader = get_object_or_404(Profile, id=account.leader.id)
		leader.count -= 1
		leader.save()

		action = Action(leader = get_object_or_404(Profile, user = request.user), action = 1, account = account)
		action.save()

		return redirect('account:profile')
	else:
		return redirect('account:profile')

def actions(request):
	if request.user.is_authenticated:
		leader = get_object_or_404(Profile, user = request.user)
		actions = Action.objects.filter(leader = leader)

		now = timezone.datetime.now()
		context = {'actions': actions, 'now': now}
		return render(request, 'account/actions.html', context)
	else:
		return redirect('account:profile')

def contact(request):
	if request.user.is_authenticated:
		return render(request, 'account/contact.html')
	else:
		return redirect('account:profile')
