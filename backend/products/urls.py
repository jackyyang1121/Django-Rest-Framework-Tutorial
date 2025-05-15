from django.urls import path

from . import views 

# /api/products/
urlpatterns = [
    path('', views.product_list_create_view, name='product-list'),  
    #views.product_list_create_view = ProductListCreateAPIView.as_view()
    path('<int:pk>/update/', views.product_update_view, name='product-edit'),
    # <int>：表示這個參數必須是整數（integer）。例如 1、42 可以，但 abc 不行。
    # pk：是你給這個參數取的名字，通常代表資料庫中的主鍵。Django 會把捕獲的值傳給視圖。
    # 例如：路徑 products/<int:pk>/，用戶訪問 /products/42/，Django 解析出 pk=42。
    path('<int:pk>/delete/', views.product_destroy_view),
    path('<int:pk>/', views.product_detail_view, name='product-detail')
]