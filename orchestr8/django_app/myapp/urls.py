from django.urls import path
from myapp.views import health_check
from . import views

urlpatterns = [
    path('healthcheck/', health_check, name='health_check'),
    path('status_page/', views.submit_task, name='status_page'),
    path('success/', views.success, name='success'),
]