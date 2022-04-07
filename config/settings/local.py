from .base import *  # noqa

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

KAKAO_REST_API_KEY = os.environ['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = os.environ['KAKAO_REDIRECT_URI']
