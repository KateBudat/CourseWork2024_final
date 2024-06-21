from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='registrations'),
    path('add_registration/', views.add_registration, name='add_registration'),
    path('mark_as_done/<int:event_id>/', views.mark_as_done, name='mark_as_done'),
    path('mark_as_cancelled/<int:event_id>/', views.mark_as_cancelled, name='mark_as_cancelled'),
    path('edit_registration/<int:id_registration>/', views.edit_registration, name='edit_registration'),
    path('delete_registration/<int:id_registration>/', views.delete_registration, name='delete_registration'),

    path('details/<int:id_registration>/', views.registration_details, name='registration_details'),
    path('add_used_material_to_registration/<int:id_registration>/<int:id_material>/',
         views.add_used_material_to_registration, name='add_used_material_to_registration'),
]