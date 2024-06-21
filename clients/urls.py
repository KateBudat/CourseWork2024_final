from django.urls import path
from . import views

urlpatterns = [
    path('', views.clients, name='clients'),
    path('add_client/', views.add_client, name='add_client'),
    path('edit_client/<int:id_client>/', views.edit_client, name='edit_client'),
    path('delete_client/<int:id_client>/', views.delete_client, name='delete_client'),
]