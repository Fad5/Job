# jobs/models.py
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title