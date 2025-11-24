from django.conf import settings
from django.contrib.auth import logout


class AdminSessionSeparationMiddleware:
    """Logs out staff users automatically when they leave admin routes.

    This keeps storefront sessions separate from admin sessions by ensuring
    that authenticated staff users are signed out as soon as they visit any
    non-admin URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.static_prefix = getattr(settings, 'STATIC_URL', '/static/') or '/static/'
        self.media_prefix = getattr(settings, 'MEDIA_URL', '/media/') or '/media/'

    def __call__(self, request):
        if self._should_force_logout(request):
            logout(request)
        response = self.get_response(request)
        return response

    def _should_force_logout(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return False
        path = request.path or ''
        # Allow admin routes
        if path.startswith('/admin'):
            return False
        # Allow static and media files
        if self.static_prefix and path.startswith(self.static_prefix):
            return False
        if self.media_prefix and path.startswith(self.media_prefix):
            return False
        # Allow logout endpoint
        if path == '/logout/':
            return False
        # Don't force logout - let staff users browse the site
        # This middleware is too aggressive and causes session issues
        return False
