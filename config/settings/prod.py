from .base import *  # noqa

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MARIADB_DATABASE'],
        'USER': 'root',
        'PASSWORD': os.environ['MARIADB_ROOT_PASSWORD'],
        'HOST': 'db',
        'PORT': '3306',
    }
}

KAKAO_REST_API_KEY = os.environ['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = os.environ['KAKAO_REDIRECT_URI']
