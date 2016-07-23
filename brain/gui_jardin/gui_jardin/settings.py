"""
Django settings for gui_jardin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#11ripgynoinwo46*ao3t5^g@1r1vgw7(xyvf2axlf9!1%sp9u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = "#MISSING OR INVALID DATA#"

    
ALLOWED_HOSTS = ["127.0.0.1/32","192.168.0.0/16", '172.16.0.0/16', '10.0.0.0/8' ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'datalogger',
    'core',
    'celery',
    'dhcp',

)

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gui_jardin.urls'

WSGI_APPLICATION = 'gui_jardin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jardin',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD':'sdrouf',
        'TEST_DEPENDENCIES': [],
    },
    'core':{
        'TEST_DEPENDENCIES': [],
        'ENGINE': 'django.db.backends.mysql',
         'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD':'sdrouf',
       'NAME': 'jardin',
        },
    'datalogger': {
        'TEST_DEPENDENCIES' : [],
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jardin',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD':'sdrouf',
        }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = './static/'
