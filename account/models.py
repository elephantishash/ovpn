from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Server(models.Model):
	ir_ip = models.CharField(max_length=20)
	fr_ip = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	count = models.IntegerField(default = 1)
	server = models.ForeignKey(Server, on_delete=models.CASCADE)
	chat_id = models.CharField(max_length=100, default='515098162')

	def __str__(self):
		return self.user.username

class Account(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=20)
	file = models.FileField(upload_to = "Accounts_file")
	cli_name = models.CharField(max_length= 100)
	created_on = models.DateTimeField(auto_now_add = True)
	date_end = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(days=30))
	leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
	server = models.ForeignKey(Server, blank=True, null=True, on_delete=models.CASCADE)
	comment = models.TextField(blank = True, null = True)
	

	def __str__(self):
		return self.name


create = 0
charge = 1

STATUS = (
    (create,"create"),
    (charge,"charge"),
)

class Action(models.Model):
	leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
	action = models.IntegerField(choices = STATUS)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add = True)
	comment = models.CharField(max_length = 200, blank = True, null = True)

	def __str__(self):
		return self.leader.user.username



# Create your models here.
