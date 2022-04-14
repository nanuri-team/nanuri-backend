from .base import *  # noqa

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
    }
}

STATIC_ROOT = BASE_DIR / 'static'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}

AWS_DYNAMODB_ENDPOINT_URL = None
AWS_DYNAMODB_ACCESS_KEY_ID = os.environ['AWS_DYNAMODB_ACCESS_KEY_ID']
AWS_DYNAMODB_SECRET_ACCESS_KEY = os.environ['AWS_DYNAMODB_SECRET_ACCESS_KEY']

KAKAO_REST_API_KEY = os.environ['KAKAO_REST_API_KEY']
KAKAO_APP_ADMIN_KEY = os.environ['KAKAO_APP_ADMIN_KEY']
KAKAO_REDIRECT_URI = os.environ['KAKAO_REDIRECT_URI']
