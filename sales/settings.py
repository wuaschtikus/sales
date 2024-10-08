"""
Django settings for sales project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/

Allauth integration
https://python.plainenglish.io/proper-way-of-using-google-authentication-with-django-and-django-allauth-part-2-c47b87dd1283
"""

import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# General
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback_secret_key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
    
# Google OICD
GOOGLE_AUTH_CLIENT_ID=os.getenv('GOOGLE_AUTH_CLIENT_ID')
GOOGLE_AUTH_CLIENT_SECRET=os.getenv('GOOGLE_AUTH_CLIENT_SECRET')
GOOGLE_AUTH_CLIENT_KEY=os.getenv('GOOGLE_AUTH_CLIENT_KEY')

# Github OIDC
GITHUB_AUTH_CLIENT_ID=os.getenv('GITHUB_AUTH_CLIENT_ID')
GITHUB_AUTH_CLIENT_SECRET=os.getenv('GITHUB_AUTH_CLIENT_SECRET')
GITHUB_AUTH_CLIENT_KEY=os.getenv('GITHUB_AUTH_CLIENT_KEY')

# Facebook OIDC
FACEBOOK_AUTH_CLIENT_ID=os.getenv('FACEBOOK_AUTH_CLIENT_ID')
FACEBOOK_AUTH_CLIENT_SECRET=os.getenv('FACEBOOK_AUTH_CLIENT_SECRET')
FACEBOOK_AUTH_CLIENT_KEY=os.getenv('FACEBOOK_AUTH_CLIENT_KEY')

# Email Settings
DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL')
DEFAULT_TO_EMAIL=os.getenv('DEFAULT_TO_EMAIL')
SERVER_EMAIL = os.getenv('SERVER_EMAIL')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

# Recaptcha Settings
# https://www.google.com/recaptcha/admin/site/707358102
RECAPTCHA_PUBLIC_KEY=os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY=os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PROXY = {}

# Stripe Checkout 
STRIPE_PAYMENT_URL_STARTER_MONTHLY=os.getenv('STRIPE_PAYMENT_URL_STARTER_MONTHLY')
STRIPE_PAYMENT_URL_PREMIUM_MONTHLY=os.getenv('STRIPE_PAYMENT_URL_PREMIUM_MONTHLY')
STRIPE_PAYMENT_URL_PRO_MONTHLY=os.getenv('STRIPE_PAYMENT_URL_PRO_MONTHLY')
STRIPE_PAYMENT_CUSTOMER_PORTAL=os.getenv('STRIPE_PAYMENT_CUSTOMER_PORTAL')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CRISPY_TEMPLATE_PACK = "bulma"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


print('Django Debug: ' + str(DEBUG))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'msgconv',
    'crispy_forms',
    'crispy_bulma',
    'users',
    'allauth', # required by allauth
    'allauth.account', # required by allauth
    'allauth.socialaccount', # required by allauth
    'allauth.socialaccount.providers.google', # required by allauth
    'allauth.socialaccount.providers.github', # required by allauth
    'allauth.socialaccount.providers.facebook', # required by allauth
    'django.contrib.humanize', # required for allauth user sessions 
    'allauth.usersessions', # required for allauth user sessions 
    "debug_toolbar", # required by django debug toolbar
    "django_recaptcha",
]

if DEBUG:
    INSTALLED_APPS.append('django.contrib.staticfiles') # makes trouble when using in prod
   
CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)

CRISPY_TEMPLATE_PACK = "bulma"

# required by debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # required for allauth
    "allauth.account.middleware.AccountMiddleware",
    # Optional -- needed when: USERSESSIONS_TRACK_ACTIVITY = True
    'allauth.usersessions.middleware.UserSessionsMiddleware',
    # required by debug toolbar
     "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': GOOGLE_AUTH_CLIENT_ID,
            'secret': GOOGLE_AUTH_CLIENT_SECRET,
            'key': GOOGLE_AUTH_CLIENT_KEY
        },
        'SCOPE': [
            'profile',
            'email',
        ]
    }, 
    'github': {
        'APP': {
            'client_id': GITHUB_AUTH_CLIENT_ID,
            'secret': GITHUB_AUTH_CLIENT_SECRET,
            'key': GITHUB_AUTH_CLIENT_KEY
        },
        'SCOPE': [
            'user',
        ],
    },
    'facebook': {
        'METHOD': 'oauth2',  # Set to 'js_sdk' to use the Facebook connect SDK
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v17.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v17.0',
        'APP': {
            'client_id': FACEBOOK_AUTH_CLIENT_ID,       
            'secret': FACEBOOK_AUTH_CLIENT_SECRET,  
            'key': FACEBOOK_AUTH_CLIENT_KEY
        }
    }
}

# https://www.pragnakalp.com/django-facebook-authentication-elevate-your-apps-security-with-this-comprehensive-guide/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout


ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_LOGOUT_URL = '/'
ACCOUNT_SESSION_REMEMBER = True
ROOT_URLCONF = 'sales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` requires the follwing 
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'sales.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
else:    
    database_url = dj_database_url.parse(os.environ.get('DATABASE_URL'))
    DATABASES = {
        'default': database_url
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG == True:
    STATIC_URL = '/static/'
else:
    STATIC_URL = '/static/'
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'sales': {  # Replace 'myapp' with your app's name
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'msgconv': {  # Replace 'myapp' with your app's name
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users': {  # Replace 'myapp' with your app's name
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}