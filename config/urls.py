# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import register_view, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),
    
    path('accounts/', include([
        path('login/', auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ), name='login'),
        
        path('logout/', auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ), name='logout'),
        
        path('register/', register_view, name='register'),
        path('register/profile/', profile_view, name='profile'),
    ])),
]