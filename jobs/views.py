# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Response
from .forms import JobForm
from django.contrib import messages
from .forms import ResponseForm

def home_view(request):
    """Главная страница - список заданий."""
    jobs = Job.objects.filter(status='open').order_by('-created_at')
    return render(request, 'home.html', {'jobs': jobs})

def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    user_has_responded = False
    
    if request.user.is_authenticated:
        user_has_responded = Response.objects.filter(
            job=job, 
            freelancer=request.user
        ).exists()
    
    return render(request, 'job_detail.html', {
        'job': job,
        'user_has_responded': user_has_responded
    })



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

@login_required
def create_response(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Проверяем условия
    if job.employer == request.user:
        messages.error(request, 'Вы не можете откликнуться на свое задание')
        return redirect('job_detail', pk=job_id)
    
    if job.status != 'open':
        messages.error(request, 'На это задание нельзя откликнуться')
        return redirect('job_detail', pk=job_id)
    
    # Проверяем, не откликался ли уже
    if Response.objects.filter(job=job, freelancer=request.user).exists():
        messages.warning(request, 'Вы уже откликнулись на это задание')
        return redirect('job_detail', pk=job_id)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.job = job
            response.freelancer = request.user
            response.save()
            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('job_detail', pk=job_id)
    else:
        form = ResponseForm()
    
    return render(request, 'response_form.html', {
        'form': form,
        'job': job
    })


@login_required
def job_responses(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    responses = job.responses.all()
    
    return render(request, 'job_responses.html', {
        'job': job,
        'responses': responses
    })