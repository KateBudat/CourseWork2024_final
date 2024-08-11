from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from clients.models import Master, ServiceDetail, Service, Registration
from users.decorators import role_required
from .forms import MasterForm
from django.db import connection
import template_views
from users.utils import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from datetime import datetime, timedelta


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def masters(request):
    query = request.GET.get('query')
    gender = request.GET.get('gender')
    active = request.GET.get('active')

    _masters = Master.objects.all().order_by('id_master')
    if active:
        _masters = _masters.filter(is_active=active)
    if query:
        _masters = _masters.filter(
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query) |
            Q(telephone_number__icontains=query) |
            Q(specialization__icontains=query)
        )
    if gender:
        _masters = _masters.filter(gender=gender)

    return render(request, 'masters/masters.html', {'masters': _masters, 'query': query, 'gender': gender})


@role_required(allowed_roles=['owner_user'])
def add_master(request):
    return template_views.add_object(request, MasterForm, 'masters/add_master.html', 'masters')


@role_required(allowed_roles=['owner_user', 'administrator_user'])
def edit_master(request, id_master):
    return template_views.edit_object(request, Master, MasterForm, 'masters/edit_master.html', 'masters', id_master)


@role_required(allowed_roles=['owner_user'])
def delete_master(request, id_master):
    try:
        master = get_object_or_404(Master, pk=id_master)
        registrations = Registration.objects.filter(service_details__master=id_master)

        if not registrations.exists():
            # Видаляємо пов'язаного користувача
            try:
                user = CustomUser.objects.get(master_id=master.id_master)
                user.delete()
            except CustomUser.DoesNotExist:
                messages.warning(request, f"Не знайдено пов'язаний користувач для майстра.")

            # Видаляємо майстра
            master.delete()
            messages.success(request, f"Майстра успішно видалено з бази даних!")
        else:
            master.is_active = False
            master.dismissal_date = date.today()
            master.save()
            messages.success(request, f"Майстра не можна видалити, але його статус змінено на неактивний!")

            # Деактивуємо користувача, пов'язаного з майстром
            try:
                user = CustomUser.objects.get(master_id=master.id_master)
                user.is_active = False
                user.save()
            except CustomUser.DoesNotExist:
                messages.warning(request, f"Не знайдено пов'язаний користувач для майстра.")

    except ObjectDoesNotExist:
        messages.error(request, "Об'єкт не існує")
    except Exception as e:
        messages.error(request, f"Виникла помилка: {str(e)}")

    return redirect('masters')


@role_required(allowed_roles=['owner_user'])
def return_master(request, id_master):
    try:
        master = Master.objects.get(pk=id_master)
        master.is_active = True
        master.dismissal_date = None
        master.save()

        try:
            user = CustomUser.objects.get(master_id=master)
            user.is_active = True
            user.save()
        except CustomUser.DoesNotExist:
            messages.warning(request, f"Не знайдено пов'язаний користувач для майстра.")

        messages.success(request, f"Майстер знову працює!")
    except ObjectDoesNotExist:
        messages.error(request, "Об'єкт не існує")
    except Exception as e:
        messages.error(request, f"Виникла помилка: {str(e)}")
    return redirect('masters')


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def get_missing_services(id_master):
    services_ids_of_master = ServiceDetail.objects.filter(master=id_master).values_list('service', flat=True)
    missing_services = Service.objects.exclude(id_service__in=services_ids_of_master)
    deleted_services = ServiceDetail.objects.filter(master=id_master, deleted=True).values_list('service', flat=True)
    missing_deleted_services = Service.objects.filter(id_service__in=deleted_services)
    return missing_services.union(missing_deleted_services).order_by('id_service')


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


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def master_services(request, id_master):
    if get_current_role() == 'master_user':
        master_user_id = request.session.get('master_user_id')
        if id_master != master_user_id:
            messages.error(request, "У вас немає права на перегляд цієї сторінки")
            return redirect('master_services', id_master=master_user_id)
    master = get_object_or_404(Master, pk=id_master)
    services = ServiceDetail.objects.filter(master=master, deleted=False).order_by('service_id')
    missing_deleted_services = get_missing_services(id_master)
    return render(request, 'masters/master_details.html', {'master': master, 'services': services,
                                                           'missing_deleted_services': missing_deleted_services})


@role_required(allowed_roles=['owner_user', 'administrator_user'])
def add_service_to_master(request, id_master, id_service):
    master = get_object_or_404(Master, id_master=id_master)
    service = get_object_or_404(Service, id_service=id_service)
    service_detail, created = ServiceDetail.objects.get_or_create(master=master, service=service)
    if not created:
        service_detail.deleted = False
        service_detail.save()
    messages.success(request, "Послугу додано до майстра!")
    return redirect('master_services', id_master=id_master)


@role_required(allowed_roles=['owner_user', 'administrator_user'])
def delete_service_detail(request, id_service_details):
    service_detail = get_object_or_404(ServiceDetail, id_service_details=id_service_details)

    # Перевірка, чи є цей service_detail в реєстраціях
    is_registered = Registration.objects.filter(service_details=service_detail).exists()

    if not is_registered:
        # Якщо service_detail ніколи не зазнався в реєстрації, видаляємо його
        service_detail.delete()
        messages.success(request, "Послугу у майстра видалено повністю!")
    else:
        # Інакше просто встановлюємо deleted=True
        service_detail.deleted = True
        service_detail.save()
        messages.success(request, "Послугу у майстра встановлено як видалену.")

    return redirect('master_services', id_master=service_detail.master.id_master)


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def analytics_master(request, id_master):
    if get_current_role() == 'master_user':
        master_user_id = request.session.get('master_user_id')
        if id_master != master_user_id:
            messages.error(request, "У вас немає права на перегляд цієї сторінки")
            return redirect('analytics_master', id_master=master_user_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Якщо дати не вказані, встановлюємо період за замовчуванням (останні 7 днів)
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_service_income_report(%s, %s, %s)", [id_master, start_date, end_date])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Обчислення сум
    total_services = sum(result['total_services_provided'] for result in results)
    total_income = sum(result['total_income'] for result in results)

    context = {
        'results': results,
        'total_services': total_services,
        'total_income': total_income,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'masters/master_analytics.html', context)
