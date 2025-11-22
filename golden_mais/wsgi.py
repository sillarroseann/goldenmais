"""
WSGI config for golden_mais project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_mais.settings')

application = get_wsgi_application()
