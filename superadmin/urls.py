from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'superadmin'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('change_server/<int:profile_id>', views.change_server, name='change_server'),
    path('charge_coin/<int:profile_id>', views.charge_coin, name='charge_coin'),
    path('server/<int:server_id>', views.server, name='server'),
    path('send_profile/<int:account_id>', views.send_profile, name='send_profile'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('create_account/', views.create_account, name='create_account'),
    path('leader_creation/', views.leader_creation, name='leader_creation'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('server_creation/', views.server_creation, name='server_creation'),
    path('create_server/', views.create_server, name='create_server'),
    path('test/', views.test, name='test'),
    path('reverse_ssh_status/<int:server_id>', views.reverse_ssh_status, name='reverse_ssh_status'),
]
