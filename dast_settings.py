from complaint_box.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dast.sqlite3',
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
