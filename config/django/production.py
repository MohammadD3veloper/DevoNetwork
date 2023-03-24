from .base import *


# Debug should be False in production mode
DEBUG = False


# Allowed hosts (Set your domain here)
ALLOWED_HOSTS = [DOMAIN_NAME, f"www.{DOMAIN_NAME}"]
# Database with postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'NAME': BASE_DIR / 'db.sqlite3',
        'HOST': env('POSTGRESQL_HOST'),
        'USER': env('POSTGRESQL_USER'),
        'PASSWORD': env('POSTGRESQL_PASSWORD'),
        'PORT': env('POSTGRESQL_PORT'),
    },
}


# Caching with redis
CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
        'LOCATION': env("REDIS_URL"),
    }
}

CACHE_TTL = 60 * 15

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'log/devo_network.log',
            'formatter': 'app',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'formatters': {
        'app': {
            'format': [
                "%(asctime)s:[%(levelname)-8s]" "(%(module)s.%(funcName)s): %(message)s"
            ],
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    }
}
