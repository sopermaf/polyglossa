"""
Modified version of settings for testing in
Github CI to avoid confusing test settings
with real site settings
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
