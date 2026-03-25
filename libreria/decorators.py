from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps


def solo_dueno(view_func):
    """Solo permite acceso a superusuarios (dueño)."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('/tienda/')  # ✅ redirige en vez de 403
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_o_dueno(view_func):
    """Permite acceso a staff y superusuarios (trabajadores y dueño)."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('/tienda/')  # ✅ redirige en vez de 403
        return view_func(request, *args, **kwargs)
    return wrapper


def es_dueno(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)