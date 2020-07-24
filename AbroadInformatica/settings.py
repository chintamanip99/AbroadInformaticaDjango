"""
Django settings for AbroadInformatica project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wewao9s!adhyl0cp&kla)gt!7xqa3nwv23-3v04*=4u5nzt9i&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# django.setup()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'content',
    'posts',
    'profiles',
    'rest_framework.authtoken',
    # 'gdstorage',
    'corsheaders',
    # 'periodically'

]

# import djcelery
# djcelery.setup_loader()
# BROKER_URL="django://"

# ##########
# LOGGING = {
#     'version':1,
#     'disable_existing_loggers':False,
    
#     # This part should be in your settings file by default.
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
        
#         # Add the following to enable logging for Periodically.
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }
##########

REST_FRAMEWORK = {
    'UNICODE_JSON': True,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1,
    'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend'
}

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True



MIDDLEWARE = [
    # 'posts.middleware.RequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XsFrameOptionsMiddleware',
    # 'posts.models.RequestExposerMiddleware',
]

CORS_ORIGIN_ALLOW_ALL=True

# CORS_ORIGIN_WHITELIST = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000"
# ]

ROOT_URLCONF = 'AbroadInformatica.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AbroadInformatica.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='cmp151999@gmail.com'
EMAIL_HOST_PASSWORD='ktsuqztzfaeyxtqa'
EMAIL_PORT=587
EMAIL_USE_TLS=True


# BROKER_URL='redis://127.0.0.1:6379/0'
# # BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# BROKER_TRANSPORT='redis'
# CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS=[os.path.join(BASE_DIR,"static")]#For development
STATIC_URL = '/static/'
MEDIA_ROOT=os.path.join(BASE_DIR,"media_cdn")
# MEDIA_ROOT="maps"
MEDIA_URL='/media/'
STATIC_ROOT=os.path.join(os.path.dirname(BASE_DIR),"static_cdn")
print("static root: ",STATIC_ROOT,"STATICFILES_DIRS=",STATICFILES_DIRS)
# print("media root: ",MEDIA_ROOT,"MEDIA_ROOT=",MEDIA_ROOT)

# print("google drive ",os.path.join(BASE_DIR,"google_drive_api")+"/cmpapp-62725-bbf789a11855.json")

# GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR,"google_drive_api","cmpapp-62725-bbf789a11855.json")
# GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'maps/'
########################################################
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
########################################################