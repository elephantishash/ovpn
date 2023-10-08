from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', views.HomeView.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
