from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'superadmin'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:profile>', views.profile, name='profile'),
    path('change_server/<int:profile_id>', views.change_server, name='change_server'),
    path('server/<int:server_id>', views.server, name='server'),
]