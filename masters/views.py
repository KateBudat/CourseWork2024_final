from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from users.models import Master, ServiceDetail, Service
from .forms import MasterForm
from django.db import connection
import template_views


# Create your views here.
def masters(request):
    query = request.GET.get('query')
    gender = request.GET.get('gender')

    _masters = Master.objects.all().order_by('id_master')
    if query:
        _masters = _masters.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(telephone_number__icontains=query)
        )
    if gender:
        _masters = _masters.filter(gender=gender)

    return render(request, 'masters/masters.html', {'masters': _masters, 'query': query, 'gender': gender})


def add_master(request):
    return template_views.add_object(request, MasterForm, 'masters/add_master.html', 'masters')


def edit_master(request, id_master):
    return template_views.edit_object(request, Master, MasterForm, 'masters/edit_master.html', 'masters', id_master)


def delete_master(request, id_master):
    return template_views.delete_object(request, Master, id_master)


def get_missing_services(id_master):
    services_ids_of_master = ServiceDetail.objects.filter(master=id_master).values_list('service', flat=True)
    missing_services = Service.objects.exclude(id_service__in=services_ids_of_master)
    deleted_services = ServiceDetail.objects.filter(master=id_master, deleted=True).values_list('service', flat=True)
    missing_deleted_services = Service.objects.filter(id_service__in=deleted_services)
    return missing_services.union(missing_deleted_services).order_by('id_service')


def master_services(request, id_master):
    master = get_object_or_404(Master, pk=id_master)
    services = ServiceDetail.objects.filter(master=master, deleted=False).order_by('service_id')
    missing_deleted_services = get_missing_services(id_master)
    return render(request, 'masters/master_details.html', {'master': master, 'services': services,
                                                           'missing_deleted_services': missing_deleted_services})


'''
def master_services(request, id_master):
    master = get_object_or_404(Master, pk=id_master)
    services = ServiceDetail.objects.filter(master=master, deleted=False).order_by('service_id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_missing_services(%s);", (id_master,))
        missing_deleted_services = cursor.fetchall()

    return render(request, 'masters/master_details.html', {'master': master, 'services': services,
                                                           'missing_deleted_services': missing_deleted_services})

'''


def add_service_to_master(request, id_master, id_service):
    if request.user.is_authenticated:
        master = get_object_or_404(Master, id_master=id_master)
        service = get_object_or_404(Service, id_service=id_service)
        service_detail, created = ServiceDetail.objects.get_or_create(master=master, service=service)
        if not created:
            service_detail.deleted = False
            service_detail.save()
        messages.success(request, "Послугу додано до майстра!")
        return redirect('master_services', id_master=id_master)
    else:
        messages.error(request, "Вам потрібно увійти у систему...")
        return redirect('home')


def delete_service_detail(request, id_service_details):
    if request.user.is_authenticated:
        service_detail = get_object_or_404(ServiceDetail, id_service_details=id_service_details)
        service_detail.deleted = True
        service_detail.save()
        messages.success(request, "Послугу у майстра видалено!")
        return redirect('master_services', id_master=service_detail.master.id_master)
    else:
        messages.error(request, "Вам потрібно увійти у систему...")
        return redirect('home')

