from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def admin_required(view_func):
    """
    Decorator that requires user to be logged in and be staff/admin
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('admin_login')
        
        if not request.user.is_staff:
            raise PermissionDenied("You don't have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def customer_required(view_func):
    """
    Decorator that requires user to be logged in and NOT be staff/admin
    Prevents admin users from accessing customer pages
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('customer_login')
        
        if request.user.is_staff:
            raise PermissionDenied("Admin users cannot access customer pages.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
