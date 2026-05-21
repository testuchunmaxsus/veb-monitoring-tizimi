"""Development sozlamalari."""
from .base import *  # noqa: F401, F403
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Email backendni konsol orqali ko'rsatish (dev rejimda)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS dev rejimida butunlay ochiq
CORS_ALLOW_ALL_ORIGINS = True
