from django.conf import settings
from django.contrib.auth import logout


class AdminSessionSeparationMiddleware:
    """Keeps admin and customer sessions completely separate.
    
    Admin users (staff=True) can only access admin routes.
    Customer users (staff=False) can only access customer routes.
    This prevents admins from accessing customer data and vice versa.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.static_prefix = getattr(settings, 'STATIC_URL', '/static/') or '/static/'
        self.media_prefix = getattr(settings, 'MEDIA_URL', '/media/') or '/media/'

    def __call__(self, request):
        # Check if user is trying to access admin routes without being staff
        if self._should_logout(request):
            logout(request)
        response = self.get_response(request)
        return response

    def _should_logout(self, request):
        """Logout users trying to access routes they shouldn't"""
        if not request.user.is_authenticated:
            return False
        
        path = request.path or ''
        
        # Allow static and media files for everyone
        if self.static_prefix and path.startswith(self.static_prefix):
            return False
        if self.media_prefix and path.startswith(self.media_prefix):
            return False
        
        # Allow login/logout/register pages for everyone
        if path in ['/login/', '/logout/', '/register/', '/admin-login/', '/admin-register/']:
            return False
        
        # If user is NOT staff and tries to access admin routes, logout
        if path.startswith('/admin') and not request.user.is_staff:
            return True
        
        return False
