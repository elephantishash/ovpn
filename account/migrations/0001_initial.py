# Generated by Django 4.1.4 on 2023-03-14 21:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=20)),
                ('file', models.FileField(upload_to='Accounts_file')),
                ('cli_name', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('date_end', models.DateTimeField(default=datetime.datetime(2023, 4, 14, 1, 15, 18, 456890))),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ir_ip', models.CharField(max_length=20)),
                ('fr_ip', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.server')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(0, 'create'), (1, 'charge')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile'),
        ),
    ]
