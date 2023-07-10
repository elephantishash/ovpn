from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from account.models import Profile, Account, Action, Server
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

	document_sender(profile.chat_id, '{}/cli/{}/{}.ovpn'.format(current_dir, server_ip, account_name), pas)

	action = Action(leader = profile, action = 0, account = account)
	action.save()

def home(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profiles = Profile.objects.all()
			servers = Server.objects.all()
			accounts = Account.objects.all()

			print(request.META['HTTP_REFERER'])

			admin_accounts = Account.objects.filter(leader=get_object_or_404(Profile, user=request.user)).order_by('-date_end')

			context = { 'profiles': profiles,
				'servers': servers,
				'accounts': accounts,
				'admin_accounts': admin_accounts,
			}


			return render(request, 'superadmin/home.html', context=context)
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def admin_profile(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profiles = Profile.objects.all()
			servers = Server.objects.all()
			accounts = Account.objects.all()

			admin_accounts = Account.objects.filter(leader=get_object_or_404(Profile, user=request.user)).order_by('-date_end')

			context = {'profiles': profiles,
				'servers': servers,
				'accounts': accounts,
				'admin_accounts': admin_accounts,
			}
			return render(request, 'superadmin/manage.html', context = context)
	else:
		return redirect('account:login_view')

def profile(request, profile_id):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profile = get_object_or_404(Profile, id=profile_id)
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
			server = get_object_or_404(Server, ir_ip=request.POST['server_shift'])
			profile.server = server
			profile.save()
			return redirect('superadmin:profile', profile_id)
	else:
		return redirect('account:login_view')

def charge_coin(request, profile_id):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			profile = get_object_or_404(Profile, id=profile_id)
			charge_coin = request.POST['charge_coin']
			profile.count = int(charge_coin)
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

			try:
				get_object_or_404(Account, name=account_name)
				messages.add_message(request, messages.INFO, 'This name already taken')
			except:
				if account_name != "":
					server = get_object_or_404(Server, ir_ip=request.POST['server_shift'])
					profile = get_object_or_404(Profile, user=request.user)

					account_generator(profile, server, account_name)
				else:
					messages.add_message(request, messages.INFO, 'Chose somename and donnot leave it blank !')

			return redirect('superadmin:home')
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def test(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			un = request.POST['username']
			password = request.POST['password']

			cn = request.POST['count']
			si = request.POST['server_ip']

			print(un, password, cn, si)

			return redirect('superadmin:leader_creation')
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def send_profile(request, account_id):
	if request.user.is_authenticated:
		account = get_object_or_404(Account, id=account_id)
		profile = get_object_or_404(Profile, user=request.user)

		document_sender(profile.chat_id, '{}{}'.format(current_dir, account.file.url), account.password)

		return redirect('account:profile')
	else:
		return redirect('account:profile')

def leader_creation(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			servers = Server.objects.all()
			context = {
				'servers': servers,
			}

			return render(request, 'superadmin/leader_creation.html', context=context)
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def create_profile(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			username = request.POST['username']
			password = request.POST['password']

			count = request.POST['count']
			server_ip = request.POST['server_ip']

			user = User.objects.create_user(username=username, password=password)
			user.save()

			server = get_object_or_404(Server, ir_ip=server_ip)
			profile = Profile(user=user, count = int(count), server = server)
			profile.save()

			return redirect('superadmin:home')
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def server_creation(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			servers = Server.objects.all()
			context = {
				'servers': servers,
			}

			return render(request, 'superadmin/server_creation.html', context=context)
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')

def create_server(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			server_name = request.POST['server_name']
			ir_ip = request.POST['ir_ip']
			fr_ip = request.POST['fr_ip']

			next_server_ip = request.POST['next_server_ip']
			shift_server = get_object_or_404(Server, ir_ip=next_server_ip)

			server = Server(name=server_name, ir_ip=ir_ip, fr_ip=fr_ip, next_server=shift_server)
			server.save()

			return redirect('superadmin:home')
		else:
			return redirect('account:profile')
	else:
		return redirect('account:login_view')
