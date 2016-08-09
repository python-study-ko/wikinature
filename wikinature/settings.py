# -*- coding: utf-8 -*-

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ini파일 호출
from configparser import RawConfigParser
config = RawConfigParser()
config.read(os.path.join(BASE_DIR, 'settings.ini'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('deploy','SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if config.get('deploy','DEBUG') == "True":
    DEBUG = True
elif config.get('deploy','DEBUG') == "False":
    DEBUG = False

ALLOWED_HOSTS = [config.get('deploy','ALLOWED_HOSTS')]



# Application definition

INSTALLED_APPS = [
    # django base admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # 디버깅 툴바
    'debug_toolbar',
    # werkzeug 디버거를 위한 추가
    'django_extensions',
    # 제작 앱
    'main', # 메인 페이지 앱
    'namechecker', # 식물명 체크 앱
]

MIDDLEWARE_CLASSES = [
    # 디버깅 툴바 추가
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 기존코드
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# switch whitenoise : CDN사용 여부에 따라 설정파일에서 whitenoise를 켜고 끌수있게 만들어준다.
if config.get('deploy','WHITENOISE')=='True':
    # 'django.middleware.security.SecurityMiddleware'아래에 whitenoise 미들웨어 클래스가 위치해야 한다
    posithon = MIDDLEWARE_CLASSES.index('django.middleware.security.SecurityMiddleware')+1
    MIDDLEWARE_CLASSES.insert(posithon,'whitenoise.middleware.WhiteNoiseMiddleware')
elif config.get('deploy','WHITENOISE')=='False':
    pass

ROOT_URLCONF = 'wikinature.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'wikinature.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': config.get('db','ENGINE'),
        'NAME': config.get('db','NAME'),
        'USER': config.get('db','USER'),
        'PASSWORD': config.get('db','PASSWORD'),
        'HOST': config.get('db','HOST'),
        'POST': config.get('db','POST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# 한국 설정
LANGUAGE_CODE = config.get('language','LANGUAGE_CODE')
TIME_ZONE = config.get('language','TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 디버깅 툴바(djdt) 설정
INTERNAL_IPS = ['127.0.0.1']

NAME_APIKEY = config.get('api','NAME_APIKEY')
