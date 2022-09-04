from .base import *  # noqa

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

THIRD_PARTY_APPS += [
    "django_extensions",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": "db",
        "PORT": "5432",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    }
}
