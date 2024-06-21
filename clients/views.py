from django.shortcuts import render
from django.db.models import Q
from users.models import Client
from .forms import ClientForm
import template_views


def clients(request):
    query = request.GET.get('query')
    gender = request.GET.get('gender')

    _clients = Client.objects.all().order_by('id_client')
    if query:
        _clients = _clients.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(telephone_number__icontains=query)
        )
    if gender:
        _clients = _clients.filter(gender=gender)

    return render(request, 'clients/clients.html', {'clients': _clients, 'query': query, 'gender': gender})


def add_client(request):
    return template_views.add_object(request, ClientForm, 'clients/add_client.html', 'clients')


def edit_client(request, id_client):
    return template_views.edit_object(request, Client, ClientForm, 'clients/edit_client.html', 'clients', id_client)


def delete_client(request, id_client):
    return template_views.delete_object(request, Client, id_client)
