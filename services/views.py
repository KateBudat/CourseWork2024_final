from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Service
from .forms import ServiceForm
import template_views


# Create your views here.
def services(request):
    query = request.GET.get('query')
    type_service = request.GET.get('type_service')

    _services = Service.objects.all().order_by('id_service')
    '''
    if query:
        _services = _services.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(first_name__icontains=query.split(' ')[0], second_name__icontains=query.split(' ')[1]) |
            Q(first_name__icontains=query.split(' ')[1], second_name__icontains=query.split(' ')[0]) |
            Q(telephone_number__icontains=query)
        )
     '''
    if type_service:
        _services = _services.filter(type_service=type_service)

    return render(request, 'services/services.html', {'services': _services, 'query': query, 'type_service': type_service})


def add_service(request):
    return template_views.add_object(request, ServiceForm, 'services/add_service.html', 'services')


def edit_service(request, id_service):
    return template_views.edit_object(request, Service, ServiceForm, 'services/edit_service.html', 'services', id_service)


def delete_service(request, id_service):
    return template_views.delete_object(request, Service, id_service)

