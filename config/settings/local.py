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

STATIC_ROOT = BASE_DIR / 'static'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    }
}

AWS_DYNAMODB_ENDPOINT_URL = 'http://localhost:8000'
AWS_DYNAMODB_ACCESS_KEY_ID = None
AWS_DYNAMODB_SECRET_ACCESS_KEY = None

KAKAO_REST_API_KEY = os.environ['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = os.environ['KAKAO_REDIRECT_URI']
