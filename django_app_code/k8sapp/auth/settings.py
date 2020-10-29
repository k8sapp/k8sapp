"""
Django settings for auth project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v!5j@_!&g4ae+rc*@!#4b(=w1&63(e4@df820oo%)g-!=36bm1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
## following code suggests being able to get hostname address programmatically
## but getting error with it

#from kubernetes import client, config

#config.load_incluster_config()
#v1=client.CoreV1Api()
#for address in v1.read_node(os.environ['HOSTNAME']).status.addresses:
#    if address.type == 'ExternalIP':
#        print(address.address)

from socket import gethostname, gethostbyname
print("get host by name: ", gethostname())
print("get host by name: ", gethostbyname(gethostname()))
print("HOST IP: ", os.environ.get('HOST_IP'))
#ALLOWED_HOSTS = [gethostname(), gethostbyname(gethostname()), "*"]
ALLOWED_HOSTS = [gethostname(), gethostbyname(gethostname()), "localhost", "127.0.0.1", "0.0.0.0", "*"]
#ALLOWED_HOSTS = [os.environ.get('HOST_IP'), '127.0.0.1']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # New app
    'socialauth',
    # Required for allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # apps for storage of static files
    'storages',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth.urls'

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

WSGI_APPLICATION = 'auth.wsgi.application'


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


# Add the following
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
 
]

LOGIN_REDIRECT_URL = '/'


# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
##STATIC_URL = '/static/'
##STATIC_ROOT = os.path.join(BASE_DIR, "static")
##MEDIA_ROOT = os.path.join(BASE_DIR, "media")

## Read static files from COS (or in the future from CDN)
USE_COS = os.getenv('USE_COS') == 'TRUE'

# https://webapp-jkactivai.s3.us.cloud-object-storage.appdomain.cloud/static/
print("USE COS: ", os.getenv('USE_COS'))
if USE_COS:
  # COS credentials
  AWS_ACCESS_KEY_ID = os.getenv('COS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.getenv('COS_SECRET_ACCESS_KEY')
  AWS_STORAGE_BUCKET_NAME = os.getenv('COS_BUCKET_NAME')
  AWS_DEFAULT_ACL = 'public-read'
  COS_ENDPOINT = os.getenv('COS_ENDPOINT')
  # COS static settings
  COS_DIR = 'static'
  AWS_LOCATION = 'static'
  AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{COS_ENDPOINT}'
  AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

  #STATIC_URL = f'https://{COS_ENDPOINT}/{COS_BUCKET_NAME}/{COS_DIR}/'
  #STATIC_URL = f'https://{COS_BUCKET_NAME}.{COS_ENDPOINT}/{COS_DIR}/'
  STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/' 
  STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
  print('static file storage: ', STATICFILES_STORAGE)
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#print('COS ACCESS KEY ID: ', COS_ACCESS_KEY_ID)
#print('COS SECRET ACCESS KEY: ', COS_SECRET_ACCESS_KEY)
#print('COS BUCKET NAME: ', COS_BUCKET_NAME)
#print('AWS Default ACL: ', AWS_DEFAULT_ACL)
#print('COS ENDPOINT: ', COS_ENDPOINT)
#print('COS DIR: ', COS_DIR)
print('static url: ', STATIC_URL)

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, ' mediafiles')






