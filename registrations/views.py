from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from materials.forms import UsedMaterialForm
from materials.views import get_material_with_info
from template_views import *
from clients.models import *
"""
    TO DO:
    - Додати кольори для подій, які очікуються, виконані, скасовані
    - Додати фільтр по майстрам, по статусу
"""


def calendar_view(request):
    master_id = request.GET.get('master')
    status = request.GET.get('status')

    registrations = Registration.objects.all()
    masters = Master.objects.all()

    if master_id:
       registrations = registrations.filter(service_details__master=master_id)

    if status:
       registrations = registrations.filter(status=status)

    events = []

    for registration in registrations:
        start_datetime = datetime.combine(registration.registration_date, registration.start_time)
        duration = timedelta(minutes=registration.service_details.service.time_service)
        end_datetime = start_datetime + duration
        color = '#92C7CF'
        if registration.status == "Виконано":
            color = '#AFD198'
        elif registration.status == "Скасовано":
            color = '#D37676'
        events.append({
            'id': registration.id_registration,
            'title': f"{registration.client.first_name} {registration.client.second_name} - {registration.service_details.service.name_service}",
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'color': color,
            'master_id': registration.service_details.master.id_master,
            'master_first_name': registration.service_details.master.first_name,
            'master_second_name': registration.service_details.master.second_name,
            'client': f"{registration.client.first_name} {registration.client.second_name}",
            'service': registration.service_details.service.name_service,
            'master': f"{registration.service_details.master.first_name} {registration.service_details.master.second_name}",
            'cost': f"{registration.service_details.service.cost_service}",
            'percent': f"{registration.service_details.service.percent_for_master}",
            'status': registration.status,
        })

    context = {
        'events': events,
        'masters': masters,
    }
    return render(request, 'registration/calendar.html', context)


def add_registration(request):
    clients = Client.objects.all()
    services = Service.objects.all()
    service_details = ServiceDetail.objects.select_related('service', 'master').all().filter(deleted=False)

    if request.method == 'POST':
        client_id = request.POST.get('client')
        registration_date = request.POST.get('registration_date')
        start_time = request.POST.get('start_time')
        service_details_id = request.POST.get('service_details')

        try:
            client = Client.objects.get(id_client=client_id)
            service_detail = ServiceDetail.objects.get(id_service_details=service_details_id)

            status = 'Очікується'

            registration = Registration(
                client=client,
                registration_date=registration_date,
                start_time=start_time,
                service_details=service_detail,
                status=status
            )
            registration.save()

        except Exception as e:
            error_message = str(e)
            return render(request, 'registration/add_registration.html', {
                'clients': clients,
                'services': services,
                'service_details': service_details,
                'error_message': error_message
            })

        return redirect('registrations')

    return render(request, 'registration/add_registration.html', {
        'clients': clients,
        'services': services,
        'service_details': service_details,
    })


def edit_registration(request, id_registration):
    registration = Registration.objects.get(pk=id_registration)
    clients = Client.objects.all()
    services = Service.objects.all()
    service_details = ServiceDetail.objects.select_related('service', 'master').all()

    if request.method == 'POST':
        client_id = request.POST.get('client')
        registration_date = request.POST.get('registration_date')
        start_time = request.POST.get('start_time')
        service_details_id = request.POST.get('service_details')

        client = Client.objects.get(id_client=client_id)
        service_detail = ServiceDetail.objects.get(id_service_details=service_details_id)

        registration.client = client
        registration.registration_date = registration_date
        registration.start_time = start_time
        registration.service_details = service_detail

        try:
            registration.save()
        except Exception as e:
            error_message = str(e)
            return render(request, 'registration/edit_registration.html', {
                'clients': clients,
                'service_details': service_details,
                'registration': registration,
                'error_message': error_message
            })

        return redirect('registrations')

    return render(request, 'registration/edit_registration.html', {
        'clients': clients,
        'services': services,
        'service_details': service_details,
        'registration': registration,
    })


def mark_as_done(request, event_id):
    try:
        registration = Registration.objects.get(pk=event_id)
        registration.status = 'Виконано'
        registration.save()
        messages.success(request, "Подію відмічено як виконану.")
    except Registration.DoesNotExist:
        messages.error(request, "Подію не знайдено.")

    return redirect('registrations')


def mark_as_cancelled(request, event_id):
    try:
        registration = Registration.objects.get(pk=event_id)
        registration.status = 'Скасовано'
        registration.save()
        messages.success(request, "Подію відмічено як скасовану.")
    except Registration.DoesNotExist:
        messages.error(request, "Подію не знайдено.")

    return redirect('registrations')


def delete_registration(request, id_registration):
    return delete_object(request, Registration, id_registration)


def get_unused_materials(id_registration):
    # Отримуємо ідентифікатори використаних матеріалів
    used_material_ids = Used_Material.objects.filter(registration=id_registration).values_list('material', flat=True)
    all_materials = get_material_with_info()
    unused_materials = [
        material for material in all_materials
        if material['id_material'] not in used_material_ids
    ]

    return unused_materials


def registration_details(request, id_registration):
    registration = get_object_or_404(Registration, pk=id_registration)
    used_materials = Used_Material.objects.filter(registration=registration).order_by('id_used_material')
    available_materials = get_unused_materials(id_registration)
    return render(request, 'registration/registration_details.html',
                  {'registration': registration, 'used_materials': used_materials,
                   'available_materials': available_materials})


def add_used_material_to_registration(request, id_registration, id_material):
    if request.user.is_authenticated:
        registration = get_object_or_404(Registration, pk=id_registration)
        material = get_object_or_404(Material, pk=id_material)

        if request.method == 'POST':
            form = UsedMaterialForm(request.POST)
            if form.is_valid():
                used_amount = form.cleaned_data['used_amount']
                used_material, created = Used_Material.objects.get_or_create(
                    registration=registration,
                    material=material,
                    defaults={'used_amount': used_amount}
                )
                if not created:
                    used_material.used_amount = used_amount
                    used_material.save()
                messages.success(request, "Додано запис про викоритсаний матеріал!")
                return redirect('registration_details', id_registration=id_registration)
        else:
            form = UsedMaterialForm()

        return render(request, 'materials/used/add_used_material.html', {'form': form, 'registration': registration, 'material': material})
    else:
        messages.error(request, "Вам потрібно увійти у систему...")
        return redirect('home')
