from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', views.login_view, name='login_view'),
    path('check/', views.check, name='check'),
    path('create_account/', views.create_account, name='create_account'),
    path('charge_account/<int:account_id>', views.charge_account, name='charge_account'),
    path('actions/', views.actions, name='actions'),
    path('contact/', views.contact, name='contact'),
]