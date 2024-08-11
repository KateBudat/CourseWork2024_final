from django.shortcuts import render
from django.db.models import Q
from .models import Client
from users.decorators import role_required
from .forms import ClientForm
import template_views


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def clients(request):
    query = request.GET.get('query')
    gender = request.GET.get('gender')

    _clients = Client.objects.all().order_by('id_client')
    if query:
        _clients = _clients.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(telephone_number__icontains=query) |
            Q(note__icontains=query)
        )
    if gender:
        _clients = _clients.filter(gender=gender)

    return render(request, 'clients/clients.html', {'clients': _clients, 'query': query, 'gender': gender})


@role_required(allowed_roles=['owner_user', 'administrator_user'])
def add_client(request):
    return template_views.add_object(request, ClientForm, 'clients/add_client.html', 'clients')


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def edit_client(request, id_client):
    return template_views.edit_object(request, Client, ClientForm, 'clients/edit_client.html', 'clients', id_client)


@role_required(allowed_roles=['owner_user', 'administrator_user'])
def delete_client(request, id_client):
    return template_views.delete_object(request, Client, id_client)


def analytics_client(request, id_client):
    pass
