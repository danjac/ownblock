from configurations import Configuration, values

from os import path


class Base(Configuration):

    DJANGO_ROOT = path.dirname(path.abspath(__file__))
    SITE_ROOT = path.dirname(DJANGO_ROOT)
    SITE_NAME = path.basename(DJANGO_ROOT)

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    ADMINS = (
        ('Dan Jacob', 'danjac354@gmail.com'),
    )
    DEFAULT_FROM_EMAIL = 'noreply@ownblock.com'

    MANAGERS = ADMINS

    DB_NAME = values.Value('DB_NAME')
    DB_USER = values.Value('DB_USER')
    DB_PASSWORD = values.Value('DB_PASSWORD')

    @property
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': self.DB_NAME,
                'USER': self.DB_USER,
                'PASSWORD': self.DB_PASSWORD,
                'HOST': '127.0.0.1',
                'PORT': '',
            }
        }

    SITE_ID = 1

    TIME_ZONE = 'America/Los_Angeles'
    USE_TZ = True

    LANGUAGE_CODE = 'en-us'

    USE_I18N = True
    USE_L10N = True

    MEDIA_ROOT = path.normpath(path.join(SITE_ROOT, 'media'))
    MEDIA_URL = '/media/'

    STATIC_ROOT = path.normpath(path.join(SITE_ROOT, 'assets'))
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        path.normpath(path.join(SITE_ROOT, 'static')),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    SECRET_KEY = r"pl9^9$(h(_0w*h5!c$$t^ogv*!qr==m%6*75z2)@v$0m@@^odv"

    ALLOWED_HOSTS = []

    FIXTURE_DIRS = (
        path.normpath(path.join(SITE_ROOT, 'fixtures')),
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_DIRS = (
        path.normpath(path.join(SITE_ROOT, 'templates')),
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'ownblock.apps.buildings.middleware.CurrentBuildingMiddleware',
        'ownblock.apps.buildings.middleware.CurrentSiteMiddleware',
    )

    ROOT_URLCONF = '%s.urls' % SITE_NAME
    APPEND_SLASH = False

    DJANGO_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    )

    THIRD_PARTY_APPS = (
        'django_extensions',
        'rest_framework',
    )

    LOCAL_APPS = (
        'ownblock.apps.accounts',
        'ownblock.apps.amenities',
        'ownblock.apps.buildings',
        'ownblock.apps.complaints',
        'ownblock.apps.contacts',
        'ownblock.apps.documents',
        'ownblock.apps.messaging',
        'ownblock.apps.notices',
        'ownblock.apps.parking',
        'ownblock.apps.storage',
        'ownblock.apps.tickets',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
    WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

    AUTH_USER_MODEL = 'accounts.User'
    AUTHENTICATION_BACKENDS = (
        'ownblock.apps.accounts.backends.ObjectPermissionBackend',
    )
    LOGIN_URL = '/account/login/'
    LOGIN_REDIRECT_URL = '/app'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
            'ownblock.apps.buildings.permissions.IsBuilding',
            'rest_framework.permissions.DjangoObjectPermissions',
        )
    }

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


class Local(Base):
    DEBUG = TEMPLATE_DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    # Django Toolbar setup

    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES = Base.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    INTERNAL_IPS = ('127.0.0.1',)


class Test(Base):

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        },
    }

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'django_nose',
    )


class Production(Base):

    ALLOWED_HOSTS = ['.ownblock.com']

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = values.Value('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER = values.Value('EMAIL_HOST_USER')
    EMAIL_PORT = values.Value('EMAIL_PORT', 587)

    EMAIL_SUBJECT_PREFIX = '[%s] ' % Base.SITE_NAME
    EMAIL_USE_TLS = True

    SERVER_EMAIL = "errors@ownblock.com"

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    SECRET_KEY = values.Value('SECRET_KEY')

    @property
    def LOGGING(self):
        LOGGING = Base.LOGGING
        LOGGING['handlers']['file'] = {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': path.normpath(path.join(
                self.SITE_ROOT, 'logs', 'error.log')),
        }
        LOGGING['loggers']['django.request']['handlers'].append('file')
        return LOGGING
