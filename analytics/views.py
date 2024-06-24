from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta
from users.decorators import role_required


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def analytics(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    client_service = client_service_stats(start_date, end_date)
    master_service = master_service_stats(start_date, end_date)
    service_registration = service_registration_stats(start_date, end_date)
    material = material_stats(start_date, end_date)

    context = {
        'client_service': client_service,
        'master_service': master_service,
        'service_registration': service_registration,
        'material': material,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'analytics/analytics.html', context)


def execute_stats_query(proc_name, start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {proc_name}(%s, %s)', [start_date, end_date])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


def client_service_stats(start_date, end_date):
    return execute_stats_query('client_service_stats', start_date, end_date)


def master_service_stats(start_date, end_date):
    return execute_stats_query('master_service_stats', start_date, end_date)


def service_registration_stats(start_date, end_date):
    return execute_stats_query('service_registration_stats', start_date, end_date)


def material_stats(start_date, end_date):
    return execute_stats_query('material_stats', start_date, end_date)


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




