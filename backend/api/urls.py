from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# 可以把 TokenObtainPairView 看作一個預寫好的功能模組，類似 Pandas 提供數據處理工具
# 這裡它是專門用來驗證用戶憑證（像用戶名和密碼），然後生成 token。

from . import views
# from .views import api_home


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Django 的類視圖（像 TokenObtainPairView）需要通過 as_view() 轉換，才能在 URL 路由中被正確使用。
    # 它會處理 HTTP 請求（像 POST）並調用類中的對應方法。
    # name='token_obtain_pair' 是給這個 URL 路徑取一個名字，方便在程式碼中引用這個路徑。
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', views.api_home), # localhost:8000/api/
    # path('products/', include('products.urls'))
]


"""
為什麼要用 as_view() 轉換？
想像 Django 是一個工廠，工廠只認識「工人」（函數視圖），但 TokenObtainPairView 是一個「藍圖」（類）。
工廠看不懂藍圖，得先把藍圖轉成一個工人才能用。as_view() 就是把藍圖轉成工人的工具。
"""