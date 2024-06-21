from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name='services'),
    path('add_service/', views.add_service, name='add_service'),
    path('edit_service/<int:id_service>/', views.edit_service, name='edit_service'),
    path('delete_client/<int:id_service>/', views.delete_service, name='delete_service'),
]