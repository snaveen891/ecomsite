from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('set_password/', views.set_password, name='set_password'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    
]