# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register_view(request):
    """Регистрация."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    """Профиль пользователя."""
    return render(request, 'profile.html', {'user': request.user})