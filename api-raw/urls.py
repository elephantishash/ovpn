from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.getData),
]

urlpatterns = format_suffix_patterns(urlpatterns)
