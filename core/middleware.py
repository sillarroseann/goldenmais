from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class AdminSessionSeparationMiddleware:
    """Keeps admin and customer sessions completely separate.
    
    Admin users (staff=True) can ONLY access admin routes.
    Customer users (staff=False) can ONLY access customer routes.
    This prevents admins from accessing customer data and vice versa.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.static_prefix = getattr(settings, 'STATIC_URL', '/static/') or '/static/'
        self.media_prefix = getattr(settings, 'MEDIA_URL', '/media/') or '/media/'

    def __call__(self, request):
        # Check if user is trying to access routes they shouldn't
        redirect_response = self._check_access_violation(request)
        if redirect_response:
            return redirect_response
        
        response = self.get_response(request)
        return response

    def _check_access_violation(self, request):
        """Enforce strict separation between admin and customer routes"""
        if not request.user.is_authenticated:
            return None
        
        path = request.path or ''
        
        # Allow static and media files for everyone
        if self.static_prefix and path.startswith(self.static_prefix):
            return None
        if self.media_prefix and path.startswith(self.media_prefix):
            return None
        
        # Allow login/logout/register pages for everyone
        if path in ['/login/', '/logout/', '/register/', '/admin-login/', '/admin-register/']:
            return None
        
        # ADMIN ROUTES - Only staff users allowed
        admin_routes = ['/admin', '/admin-dashboard', '/admin-orders', '/admin-products', 
                       '/admin-customers', '/admin-messages', '/admin-support']
        is_admin_route = any(path.startswith(route) for route in admin_routes)
        
        if is_admin_route:
            if not request.user.is_staff:
                # Customer trying to access admin route - logout and redirect
                logout(request)
                return redirect('customer_login')
            return None
        
        # CUSTOMER ROUTES - Only non-staff users allowed
        customer_routes = ['/', '/products', '/product', '/cart', '/checkout', '/profile', 
                          '/order-history', '/buy-now', '/add-to-cart', '/update-cart']
        is_customer_route = any(path.startswith(route) for route in customer_routes)
        
        if is_customer_route:
            if request.user.is_staff:
                # Admin trying to access customer route - logout and redirect
                logout(request)
                return redirect('admin_login')
            return None
        
        return None
