from django.urls import path
from . import views

urlpatterns = [
    path('', views.masters, name='masters'),
    path('add_master/', views.add_master, name='add_master'),
    path('edit_master/<int:id_master>/', views.edit_master, name='edit_master'),
    path('delete_master/<int:id_master>/', views.delete_master, name='delete_master'),
    path('details/<int:id_master>/', views.master_services, name='master_services'),
    path('add_service_to_master/<int:id_master>/<int:id_service>/', views.add_service_to_master, name='add_service_to_master'),
    path('delete_service_detail/<int:id_service_details>/', views.delete_service_detail, name='delete_service_detail'),
]