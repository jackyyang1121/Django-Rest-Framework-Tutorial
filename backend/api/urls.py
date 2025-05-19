from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# 可以把 TokenObtainPairView 看作一個預寫好的功能模組，類似 Pandas 提供數據處理工具
# 這裡它是專門用來驗證用戶憑證（像用戶名和密碼），然後生成 token。

# 這裡是從backend/api/views.py 導入 api_home 函數視圖
from . import views


#http://localhost:8000/api/
urlpatterns = [
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Django 的類視圖（像 TokenObtainPairView）需要通過 as_view() 轉換，才能在 URL 路由中被正確使用。
    # 它會處理 HTTP 請求（像 POST）並調用類中的對應方法。
    # name='token_obtain_pair' 是給這個 URL 路徑取一個名字，方便在程式碼中引用這個路徑。
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.api_home), # localhost:8000/api/
    # path('products/', include('products.urls'))
]

"""
TokenObtainPairView 來自 rest_framework_simplejwt.views，as_view() 來自 Django 的 View。
"""
"""
為什麼要用 as_view() 轉換？
想像 Django 是一個工廠，工廠只認識「工人」（函數視圖），但 TokenObtainPairView 是一個「藍圖」（類）。
工廠看不懂藍圖，得先把藍圖轉成一個工人才能用。as_view() 就是把藍圖轉成工人的工具。
TokenObtainPairView 是個工具，負責驗證用戶 (如帳號密碼) 並生成 token。
as_view() 把它包裝成 Django 路由能認的函數，這樣用戶訪問某 URL (如 /token/) 就能觸發它，拿到 token。
"""
"""
TokenObtainPairView 返回一對 JWT token (access token 和 refresh token)。
例子：
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
"""
"""
為什麼要 refresh token，而不是只用 access 就好？
答案：
只用 access token 會導致安全性和用戶體驗的問題，refresh token 解決了這些問題。
使用兩個 token（access 和 refresh）是為了平衡安全性和用戶體驗。access token 用於認證，refresh token 用於獲取新的 access token。
細節：
安全性：如果 access token 有效期很長（例如 1 個月），一旦被竊取，攻擊者可以長期使用，風險很高。讓 access token 短命（例如 5 分鐘）可以降低風險，但這會讓用戶頻繁重新登入，影響體驗。
用戶體驗：refresh token 有效期長（例如 1 天），可以在 access token 過期時自動獲取新的 access token，無需用戶再次輸入帳號密碼。
這種設計（短期的 access + 長期的 refresh）在安全性和便利性之間找到平衡。
"""
"""
簡單講就是，讓access token可以一直換(每五分鐘)防止被竊取，而refresh token則是讓他可以自動索取新的token所以用戶不用一直重新登入
但一到refresh更新的時間(一天)就還是要用戶重新登入索取新的一組
"""