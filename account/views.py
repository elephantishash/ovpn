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
import requests
import os

current_dir = os.getcwd()

def document_sender(chat_id, file, caption):
	apiToken = '6292864503:AAHSpBSym2NVJuubNdfmuUFCxf5z-i8Gpnc'
	apiURL = f'https://api.telegram.org/bot{apiToken}/sendDocument'
	files = {'document': open(file,'rb')}
	data = {'chat_id': chat_id, 'parse_mode':'HTML', 'caption':caption}
	r = requests.post(apiURL, data=data, files=files, stream=True)
	return r.json()

def message_sender(message, chat_id):
	apiToken = '6292864503:AAHSpBSym2NVJuubNdfmuUFCxf5z-i8Gpnc'
	apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
	data = {'chat_id': chat_id, 'text': message}
	r = requests.post(apiURL, data=data)
	return r.json()

def profile(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return redirect('superadmin:home')
		else:
			profile = get_object_or_404(Profile, user = request.user)
			accounts = Account.objects.filter(leader=profile).order_by('-date_end')
			accounts_count = accounts.count()
			coins = profile.count
			today = timezone.datetime.today().day

			if profile.chat_id == "515098162":
				messages.add_message(request, messages.INFO, 'Please enter your Telegram Chat ID in edit section')

			context = {'profile': profile,
				'accounts': accounts,
				'coins': coins,
				'accounts_count': accounts_count,
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

def create_ssh_config(username, password, expdate):
	token = '1693053954X7H0C3M46ETKGSY'
	url = "https://cofee.fdlock.xyz:1978/api/adduser"

	j = {'token': token, 'username': username, 'password': password, 'multiuser': '1', 'traffic': '50', 'type_traffic': 'gb', 'expdate': expdate}
	x = requests.post(url, json=j)
	return x

def account_generator(profile, server_ip, account_name):
	none_name = ''
	for i in os.listdir('{}/cli/{}'.format(current_dir, server_ip)):
		if i.startswith('cli_'):
			none_name = i
			break

	if none_name != '':
		global pas
		pas = ''
		with open('{}/cli/{}/pass.txt'.format(current_dir, server_ip), 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line.startswith(none_name):
					pas = line.split(' : ')[1]

		os.rename('{}/cli/{}/{}'.format(current_dir, server_ip, none_name), '{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name))
		with open('{}/cli/{}/{}.ovpn'.format(current_dir,server_ip, account_name), 'rb') as f:
			ovpn_file = File(f)
			ovpn_file = File(f, name=os.path.basename('{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name)))
			account = Account(name=account_name, password = pas, file = ovpn_file, server = profile.server, cli_name = none_name.split('.')[0], leader = profile)
			account.save()

		create_ssh_config(account.name, account.password, account.date_end.strftime("%Y-%m-%d"))
		document_sender(profile.chat_id, '{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name), pas)
		m = "Host: cofee.fdlock.xyz\nport: 22\nusername: {}\npassword: {}".format(account.name, account.password)
		message_sender(m, profile.chat_id)
		os.remove('{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name))

		action = Action(leader = profile, action = 0, account = account)
		action.save()

		message = '{}: create > {}'.format(profile, account)
		message_sender(message, '515098162')

		return True
	else:
		return False

def create_account(request):
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user = request.user)
		if profile.count != 0:
			account_name = request.POST['account_name']

			try:
				get_object_or_404(Account, name=account_name)
				messages.add_message(request, messages.INFO, 'This name already taken')
			except:
				if account_name != "":
					server_ip = profile.server.ir_ip

					if account_generator(profile, server_ip, account_name):
						profile.count -= 1
						profile.save()

					else:
						#send notif to admin for charging server
						messages.add_message(request, messages.INFO, 'There is no raw account on your server, please wait until admin charge it again')
				else:
					messages.add_message(request, messages.INFO, 'Chose somename and donnot leave it blank !')

	return redirect('account:profile')

def charge_account(request, account_id):
	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		if profile.count != 0:
			account = get_object_or_404(Account, id=account_id)
			account.date_end += datetime.timedelta(days=30)
			account.save()


			profile.count -= 1
			profile.save()

			action = Action(leader = get_object_or_404(Profile, user = request.user), action = 1, account = account)
			action.save()

			message = '{}: charge > {}'.format(profile, account)
			message_sender(message, '515098162')

		return redirect('account:profile')
	else:
		return redirect('account:profile')

def send_profile(request, account_id):
	if request.user.is_authenticated:
		account = get_object_or_404(Account, id=account_id)

		document_sender(account.leader.chat_id, '{}{}'.format(current_dir, account.file.url), account.password)

		return redirect('account:profile')
	else:
		return redirect('account:profile')

def change_chat_id(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	chat_id = request.POST['chat_id']
	print(chat_id)

	profile.chat_id = chat_id
	profile.save()

	return redirect('account:profile')

def actions(request):
	if request.user.is_authenticated:
		leader = get_object_or_404(Profile, user = request.user)
		actions = Action.objects.filter(leader = leader).order_by('date')

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
