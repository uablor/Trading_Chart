from Core.Settings.common import *



DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
if DEBUG:
    ALLOWED_HOSTS = ['*']

else:
    ALLOWED_HOSTS = ['localhost:8000','127.0.0.1:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
