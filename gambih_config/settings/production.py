# gambih_config/settings/production.py
import os
from .base import *

DEBUG = False

# Security settings - comment out for now until HTTPS is fully configured
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# Database - keep SQLite for now
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings - Directly set allowed origins
CORS_ALLOWED_ORIGINS = [
    "https://gambih.netlify.app",
    "https://bih-five.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

# Allow all origins for testing (remove after confirming working)
# CORS_ALLOW_ALL_ORIGINS = True  # Uncomment only for testing

CORS_ALLOW_CREDENTIALS = True

# Also allow these methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    'gambih.netlify.app',
    'bih-five.vercel.app',
]

# CSRF trusted origins (important for POST requests)
CSRF_TRUSTED_ORIGINS = [
    "https://gambih.netlify.app",
    "https://bih-five.vercel.app",
    "http://localhost:5173",
]



# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}