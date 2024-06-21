from django.db import connection, DatabaseError, connections
from django.conf import settings


def current_role(request):
    role = get_current_role()
    return {'current_role': role}


def get_current_role():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_role;")
            role = cursor.fetchone()[0]
        return role
    except DatabaseError as e:
        print(f"Error retrieving current role: {e}")
        return None


def change_database_credentials(new_user, new_password):
    settings.DATABASES['default']['USER'] = new_user
    settings.DATABASES['default']['PASSWORD'] = new_password
    connections['default'].close()


def set_database_connection(role):
    if role in settings.DATABASES:
        new_user = settings.DATABASES[role]['USER']
        new_password = settings.DATABASES[role]['PASSWORD']
        change_database_credentials(new_user, new_password)
    else:
        raise KeyError(f"Database settings for role '{role}' not found.")