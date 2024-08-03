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
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# get secrest keys
GOOGLE_AUTH_CLIENT_ID=os.getenv('GOOGLE_AUTH_CLIENT_ID')
GOOGLE_AUTH_CLIENT_SECRET=os.getenv('GOOGLE_AUTH_CLIENT_SECRET')
GOOGLE_AUTH_CLIENT_KEY=os.getenv('GOOGLE_AUTH_CLIENT_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l#0#!5rpz9!#^ek-3_)je%l(d_g!uh&l!ng(!#mh$bvq%us(ya'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'msgconv',
    'crispy_forms',
    'users',
    # required by allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # required for allauth user sessions 
    'django.contrib.humanize',
    'allauth.usersessions',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
    }
}
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout

# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
# ACCOUNT_PASSWORD_MIN_LENGTH = 8
# ACCOUNT_DEFAULT_HTTP_PROTOCOL='http'
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
# ACCOUNT_CHANGE_EMAIL=True

# SOCIALACCOUNT_EMAIL_REQUIRED = True
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
# SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_QUERY_EMAIL = True

#LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_URL = '/'

ACCOUNT_SESSION_REMEMBER = True


ROOT_URLCONF = 'sales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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
        },
    },
]

WSGI_APPLICATION = 'sales.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
