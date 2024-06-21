from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics, name='analytics'),
    path('clients/', views.analytics, name='client_service_stats_view'),
]