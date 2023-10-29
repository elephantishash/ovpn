from django.utils import timezone
import datetime
import requests
import os
from account.models import Profile, Account, Action, Server
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

def revoke_by_user(username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    acc_list = Account.objects.filter(leader=profile)
    now = datetime.datetime.now(timezone.utc)

    revoke_list = []
    for acc in acc_list:
        if acc.date_end < now:
            revoke_list.append(acc)

    return revoke_list



def revoke_by_server(ir_ip):
    server = get_object_or_404(Server, ir_ip=ir_ip)
    acc_list = Account.objects.filter(server=server)
    now = datetime.datetime.now(timezone.utc)

    revoke_list = []
    for acc in acc_list:
        if acc.date_end < now:
            revoke_list.append(acc)

    return revoke_list

def revoke_all():
    servers = Server.objects.all()
    now = datetime.datetime.now(timezone.utc)
    revoke_list = []
    for server in servers:
        revoke_server_cli = []
        acc_list = Account.objects.filter(server=server)
        for acc in acc_list:
            if acc.date_end < now:
                revoke_list.append(acc)
                revoke_server_cli.append(acc.cli_name.split(".")[0])
        with open("revoke_{}".format(server.ir_ip), "w") as f:
            f.write("\n".join(revoke_server_cli))

    return revoke_list


def message_sender(message, chat_id):
    apiToken = telegram_bot_token
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    r = requests.post(apiURL, data=data)
    return r.json()

def send_revoke_alert():
    leaders = Profile.objects.all()
    for leader in leaders:
        l = revoke_by_user(leader.user)
        message = "this accounts gonna to delete:\n".format(leader) + '\n'.join(i.name for i in l)
        message_sender(message, leader.chat_id)
        print(message)
