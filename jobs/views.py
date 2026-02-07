# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

def home_view(request):
    """Главная страница - список заданий."""
    jobs = Job.objects.filter(status='open').order_by('-created_at')
    return render(request, 'home.html', {'jobs': jobs})

def job_detail_view(request, pk):
    """Страница задания."""
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def job_create_view(request):
    """Создание нового задания."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    
    return render(request, 'job_form.html', {'form': form})

@login_required
def my_jobs_view(request):
    """Мои задания (созданные мной)."""
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs': jobs})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.id)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'job_edit.html', {'form': form, 'job': job})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    
    if request.method == 'POST':
        job.delete()
        return redirect('my_jobs')
    
    return render(request, 'job_delete_confirm.html', {'job': job})