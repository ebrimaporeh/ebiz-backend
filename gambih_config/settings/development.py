"""
Development settings for GAMBIH.
Uses SQLite for easy development.
"""

from .base import *

# Override DEBUG
DEBUG = True

# ============================================
# DATABASE - SQLite for development
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================
# EMAIL - Console backend for development
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================
# PASSWORD VALIDATORS - Disable for dev
# ============================================

AUTH_PASSWORD_VALIDATORS = []

# ============================================
# CORS - Allow all local origins in dev
# ============================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ============================================
# LOGGING - Enable SQL query logging
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# ============================================
# DEBUG TOOLBAR (optional)
# ============================================

if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1']
    except ImportError:
        pass