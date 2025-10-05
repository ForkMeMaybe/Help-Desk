from .common import *
import dj_database_url
import os

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")

CORS_ALLOW_ALL_ORIGINS = True

REDIS_URL = os.environ.get("REDIS_URL")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEBUG = False

DATABASES = {"default": dj_database_url.config()}


DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

SECRET_KEY = os.environ.get("SECRET_KEY")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_ROOT = BASE_DIR / "staticfiles"