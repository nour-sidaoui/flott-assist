import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret !
SECRET_KEY = '6)$fc)m8crei*l8m!8vo1sppq5(bu$s6u_#0=h(cqkt-67!6ji'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Change to shift between dev mode and deployed mode
DEPLOYED = True

ALLOWED_HOSTS = ['192.168.1.11',
                 'sidaoui.pythonanywhere.com',
                 'localhost',
                 '127.0.0.1',
                 ]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Application definition

INSTALLED_APPS = [
    # CORS
    'corsheaders',

    # my apps
    'updater.apps.UpdaterConfig',
    'conducteur.apps.ConducteurConfig',
    'dashboard.apps.DashboardConfig',
    'historique.apps.HistoriqueConfig',
    'employe.apps.EmployeConfig',
    'vehicule.apps.VehiculeConfig',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',

    # django extensions
    'django_extensions',

    # Cookie-law
    'cookielaw',

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    # DJANGO MIDDLEWARE
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ORIGIN_WHITELIST = [
    "https://localhost:8100",
    "https://127.0.0.1:8100",
]

if DEPLOYED:
    CORS_ORIGIN_WHITELIST += "https://81.249.202.21"         # <-- adding Xcode simulator ip

CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
    'POST',
]

ROOT_URLCONF = 'flott_assist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'historique/templates/historique')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'flott_assist.wsgi.application'


if DEPLOYED:
    # deployed db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sidaoui$bdd',
            'USER': 'sidaoui',
            'PASSWORD': 'python_flott_assist',
            'HOST': 'sidaoui.mysql.pythonanywhere-services.com'
        }
    }

else:
    # local db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bdd',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '8889'
        }
    }

# Socket	/Applications/MAMP/tmp/mysql/mysql.sock


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

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = False

USE_THOUSAND_SEPARATOR = True


# Static files (CSS, JavaScript, Images)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

if DEPLOYED:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

else:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

