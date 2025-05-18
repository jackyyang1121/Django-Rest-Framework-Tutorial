#當我執行 python manage.py runserver時，manage.py裡面有設定要來下載settings.py內的設定
#Django 啟動時會把這邊的設定載入到一個叫 settings 的物件裡
#先載入 settings.py，然後根據它去載入整個專案的所有東西

import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cn9t#dfjhxs%_cyenom8%qjkj=m^n(@0z85itbf+9f)o-d_13q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    #啟用Django內建的admin功能，提供管理員介面
    'django.contrib.admin',
    #啟用Django內建的auth功能，提供用戶認證
    'django.contrib.auth',
    #啟用Django內建的contenttypes功能，提供內容類型
    'django.contrib.contenttypes',
    #啟用Django內建的sessions功能，提供用戶會話
    'django.contrib.sessions',
    #啟用Django內建的messages功能，提供訊息
    'django.contrib.messages',
    #啟用Django內建的staticfiles功能，提供靜態文件
    'django.contrib.staticfiles',
    # third party api services
    'algoliasearch_django',
    # third party packages
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    # internal apps
    'api',
    'articles',
    'products',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfehome.urls'
CORS_URLS_REGEX = r"^/api/.*"
CORS_ALLOWED_ORIGINS = []

if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        'http://localhost:8111',
        'https://localhost:8111',
    ]

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

WSGI_APPLICATION = 'cfehome.wsgi.application'


#資料庫設定，從models.py中的Product模型導入
#從return ProductQuerySet(self.model, using=self._db)中的using=self._db
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
         "api.authentication.TokenAuthentication",
         "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}

# environment variables -> django-dotenv -> reads .env
ALGOLIA = {
    'APPLICATION_ID': 'H63LIZ0EO7',
    'API_KEY': '48da47d859e79e339efc931743ce9d48',
    'INDEX_PREFIX': 'cfe'
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),  # 改為 5 分鐘
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),    # 改為 1 天
}