from .base import *  # noqa

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lbmy-9j9^+a#gogp5g!8-peqov^d&wcofz%dal44hq(m8ty=^z'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

AWS_DYNAMODB_ENDPOINT_URL = None
AWS_DYNAMODB_ACCESS_KEY_ID = None
AWS_DYNAMODB_SECRET_ACCESS_KEY = None

KAKAO_REST_API_KEY = ''
KAKAO_APP_ADMIN_KEY = os.environ['KAKAO_APP_ADMIN_KEY']
KAKAO_REDIRECT_URI = ''
