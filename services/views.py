from django.shortcuts import render
from django.db.models import Q
from clients.models import Service
from .forms import ServiceForm
import template_views


def filter_service(query, _services):
    _services = _services.filter(
        Q(name_service__icontains=query) |
        Q(type_service__icontains=query)
    )

    return _services


# Create your views here.
def services(request):
    query = request.GET.get('query')
    _services = Service.objects.all().order_by('id_service')
    if query:
        _services = filter_service(query, _services)
    context = {
        'services': _services,
        'query': query
    }
    return render(request, 'services/services.html', context)


def add_service(request):
    return template_views.add_object(request, ServiceForm, 'services/add_service.html', 'services')


def edit_service(request, id_service):
    return template_views.edit_object(request, Service, ServiceForm, 'services/edit_service.html', 'services',
                                      id_service)


def delete_service(request, id_service):
    return template_views.delete_object(request, Service, id_service)
