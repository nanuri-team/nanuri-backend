from .base import *  # noqa

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS += [
    'storages',
]

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}

AWS_DYNAMODB_ENDPOINT_URL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_ACCESS_KEY_ID = os.environ['AWS_S3_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = os.environ['AWS_S3_SECRET_ACCESS_KEY']
AWS_S3_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'
