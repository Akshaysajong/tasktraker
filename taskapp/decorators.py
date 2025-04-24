from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login_user')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login_user')

        userprofile = getattr(request.user, 'userprofile', None)
        if userprofile and userprofile.user_type in ['admin', 'superadmin']:
            return view_func(request, *args, **kwargs)

        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login_user')

    return wrapper