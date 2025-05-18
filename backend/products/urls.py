from django.urls import path

from . import views 

# /api/products/
urlpatterns = [
    path('', views.product_list_create_view, name='product-list'),  
    #views.product_list_create_view = ProductListCreateAPIView.as_view()
    path('<int:pk>/update/', views.product_update_view, name='product-edit'),
    # <int>：表示這個參數必須是整數（integer）。例如 1、42 可以，但 abc 不行。
    #這行會配對product/serializers.py的get_edit_url()，再從裡面得到完整url
    path('<int:pk>/delete/', views.product_destroy_view),
    path('<int:pk>/', views.product_detail_view, name='product-detail')
]
#這邊用到的pk都是產品的pk