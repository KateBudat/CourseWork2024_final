from django.urls import path
from . import views

urlpatterns = [
    path('', views.materials, name='materials'),
    path('add_material/', views.add_material, name='add_material'),
    path('edit_material/<int:id_material>/', views.edit_material, name='edit_material'),
    path('delete_material/<int:id_material>/', views.delete_material, name='delete_material'),

    path('add_purchased_material/<int:id_material>/', views.add_purchased_material, name='add_purchased_material'),
    path('edit_purchased_material/<int:id_purchased_material>/', views.edit_purchased_material, name='edit_purchased_material'),
    path('delete_purchased_material/<int:id_purchased_material>/', views.delete_purchased_material, name='delete_purchased_material'),

    path('edit_used_material/<int:id_used_material>/', views.edit_used_material, name='edit_used_material'),
    path('delete_used_material/<int:id_used_material>/', views.delete_used_material, name='delete_used_material'),

    path('add_write_off_material/<int:id_purchased_material>/', views.add_write_off_material, name='add_write_off_material'),
    path('edit_write_off_material/<int:id_write_off_material>/', views.edit_write_off_material, name='edit_write_off_material'),
    path('delete_write_off_material/<int:id_write_off_material>/', views.delete_write_off_material, name='delete_write_off_material'),

    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('edit_supplier/<int:id_supplier>/', views.edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:id_supplier>/', views.delete_supplier, name='delete_supplier'),
]