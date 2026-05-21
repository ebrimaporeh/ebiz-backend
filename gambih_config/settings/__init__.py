# gambih_config/settings/__init__.py
import os
from decouple import config

ENVIRONMENT = config('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *