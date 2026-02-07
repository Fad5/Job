# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('job/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('job/create/', views.job_create_view, name='job_create'),
    path('my-jobs/', views.my_jobs_view, name='my_jobs'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('job/<int:job_id>/respond/', views.create_response, name='create_response'),
]