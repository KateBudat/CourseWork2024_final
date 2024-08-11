from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime, timedelta
from users.decorators import role_required
from users.utils import *


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def analytics(request):
    if get_current_role() != 'owner_user':
        return redirect('registrations')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    active_tab = request.GET.get('active_tab', 'clients')

    client_service = client_service_stats(start_date, end_date)
    master_service = master_service_stats(start_date, end_date)
    service_registration = service_registration_stats(start_date, end_date)
    #material = material_stats(start_date, end_date)
    total = execute_stats_query('total_registration_stats', start_date, end_date, 'net_income DESC')

    context = {
        'client_service': client_service,
        'master_service': master_service,
        'service_registration': service_registration,
        #'material': material,
        'total': total,
        'start_date': start_date,
        'end_date': end_date,
        'active_tab': active_tab,
    }

    return render(request, 'analytics/analytics.html', context)


@role_required(allowed_roles=['owner_user'])
def execute_stats_query(proc_name, start_date, end_date, sort):
    with connection.cursor() as cursor:
        sql_query = f'SELECT * FROM {proc_name}(%s, %s) ORDER BY {sort}'
        cursor.execute(sql_query, [start_date, end_date])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return results


def client_service_stats(start_date, end_date):
    return execute_stats_query('client_service_stats', start_date, end_date, 'net_profit DESC')


def master_service_stats(start_date, end_date):
    return execute_stats_query('master_service_stats', start_date, end_date, 'completed_registrations DESC')


def service_registration_stats(start_date, end_date,):
    return execute_stats_query('service_registration_stats', start_date, end_date, 'completed_registrations DESC')


def material_stats(start_date, end_date):
    return execute_stats_query('material_stats', start_date, end_date, 'id_material')


def get_ukrainian_month(month):
    ukrainian_months = {
        1: 'Січень',
        2: 'Лютий',
        3: 'Березень',
        4: 'Квітень',
        5: 'Травень',
        6: 'Червень',
        7: 'Липень',
        8: 'Серпень',
        9: 'Вересень',
        10: 'Жовтень',
        11: 'Листопад',
        12: 'Грудень',
    }
    return ukrainian_months.get(month)




