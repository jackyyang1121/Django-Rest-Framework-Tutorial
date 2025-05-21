#當我執行 python manage.py runserver時，manage.py裡面有設定要來下載settings.py內的設定
#Django 啟動時會把這邊的設定載入到一個叫 settings 的物件裡
#先載入 settings.py，然後根據它去載入整個專案的所有東西

import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # 這行會回傳一個 Path 物件，表示當前檔案的父目錄，也就是專案的根目錄


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# 這個SECRET_KEY是Django內建的，用來加密session和csrf token
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

    # 自己創建的 apps
    'api',
    'articles',
    'products',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',#安全，目的是防止XSS攻擊
    'django.contrib.sessions.middleware.SessionMiddleware',#保存用戶的會話信息
    'corsheaders.middleware.CorsMiddleware',#允許跨域請求
    'django.middleware.common.CommonMiddleware',#處理請求
    'django.middleware.csrf.CsrfViewMiddleware',#防止CSRF攻擊
    'django.contrib.auth.middleware.AuthenticationMiddleware',#處理用戶認證
    'django.contrib.messages.middleware.MessageMiddleware',#處理訊息
    'django.middleware.clickjacking.XFrameOptionsMiddleware',#防止點擊劫持
]

ROOT_URLCONF = 'cfehome.urls'  # 根URL配置，Django 內建，來自django.conf.settings
CORS_URLS_REGEX = r"^/api/.*"  # 允許跨域的URL，CORS_URLS_REGEX來自 corsheaders 套件(有在INSTALLED_APPS裡載入)
CORS_ALLOWED_ORIGINS = []  # 允許跨域的源

if DEBUG:     #如果DEBUG為True，則允許跨域的源，意思是在開發環境下用這個而不是上面那行。    DEBUG是Django內建的變數，用來判斷是否處於開發模式
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
        'NAME': BASE_DIR / 'db.sqlite3',  #BASE_DIR是從上面導入的，表示專案根目錄
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

LANGUAGE_CODE = 'en-us'  # 語言代碼

TIME_ZONE = 'UTC'   

USE_I18N = True  

USE_L10N = True 

USE_TZ = True  


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  #預設主鍵類型，Django 內建，對應到apps.py中的default_auto_field
#白話:這行告訴 Django：「如果我建一個模型，沒特別說要用什麼主鍵，就自動用你設定的這個類型。」

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [     #这些认证类会按顺序尝试认证，如果第一个认证失败，会尝试下一个认证
        "rest_framework.authentication.SessionAuthentication",     #主要用于 Django 管理界面，不需要 token，使用浏览器的 session cookie
         "api.authentication.TokenAuthentication",   #用于处理基于 token 的认证，需要提供 token 在请求头中
         "rest_framework_simplejwt.authentication.JWTAuthentication",   #用于处理基于 JWT 的认证，需要提供 JWT token 在请求头中
    ],
    "DEFAULT_PERMISSION_CLASSES": [       
        #未登录用户可以进行读取操作（GET 请求）
        # 只有登录用户才能进行修改操作（POST, PUT, DELETE 等）
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}

# environment variables -> django-dotenv -> reads .env
ALGOLIA = {
    'APPLICATION_ID': 'H63LIZ0EO7',
    'API_KEY': '48da47d859e79e339efc931743ce9d48',
    'INDEX_PREFIX': 'cfe'   # 索引前綴，在algolia中建立索引時，會以這個前綴加上模型名稱來建立索引，結合Product模型在algolia的dashboard顯示cfe_Product
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],   # 使用Bearer token
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),  # 改為 5 分鐘，每五分鐘自動換一次access token，自動索取新token，防止token被盜用
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),    # 改為 1 天，一天換一次refresh token，需要重新登入拿新的token
}