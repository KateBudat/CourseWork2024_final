# myapp/decorators.py
from django.http import Http404
from django.shortcuts import redirect
from .utils import get_current_role


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = get_current_role()

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif user_role == 'connection_user':
                return redirect('home')
            else:
                raise Http404("Page not found")

        return _wrapped_view

    return decorator
