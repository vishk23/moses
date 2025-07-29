from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from celery import current_app
from myapp.models import BeatHealth
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from .forms import OnDemandForm
from .tasks import run_on_demand_task

# Create your views here.

def hello(request):
    return HttpResponse("Hello, World!")

@never_cache
def health_check(request):
    status = {'site': 'online'}  # Django is up if this endpoint responds
    beat_heartbeat = cache.get('beat_heartbeat')  # Retrieve from cache or database
    if beat_heartbeat and (timezone.now() - beat_heartbeat) < timedelta(minutes=15):
        status['worker'] = 'online'  # Both Beat and worker are functioning
    else:
        status['worker'] = 'offline'  # Either Beat or worker (or both) are down
    return JsonResponse(status)


def submit_task(request):
    if request.method == 'POST':
        form = OnDemandForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            key = form.cleaned_data['key']
            additions = form.cleaned_data['additions']
            deletes = form.cleaned_data['deletes']
            run_on_demand_task.delay(email, key, additions, deletes)  # Queue the task
            messages.success(request, 'Thank you for your submission. Your request is being processed.')  # Add success message
            return redirect('success')  # Redirect to success page
    else:
        form = OnDemandForm()
    return render(request, 'form.html', {'form': form})

def success(request):
    return render(request, 'success.html')

