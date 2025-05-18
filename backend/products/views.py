from rest_framework import generics, mixins
"""
generics 模組提供了一組通用視圖類（Generic Views），用於快速構建常見的 API 端點，例如列表、創建、檢索、更新或刪除資源（CRUD 操作）。 
例如：
generics.ListAPIView：用於顯示資源列表。
generics.CreateAPIView：用於創建新資源。
generics.RetrieveUpdateDestroyAPIView：用於檢索、更新或刪除單個資源。
generics.GenericAPIView：提供一個基礎視圖類，可以繼承它來實現自定義的視圖。

mixins 模組提供了一組混入類，用於為視圖添加特定功能，例如列表、創建、檢索、更新或刪除操作。這些混入類通常與 generics.GenericAPIView 結合使用。 
常見的混入類包括：
mixins.ListModelMixin：處理列表請求。
mixins.CreateModelMixin：處理創建請求。
mixins.RetrieveModelMixin：處理單個資源檢索。
"""
from rest_framework.decorators import api_view
"""
api_view 是一個裝飾器，用於將普通的 Python 函數轉換為 DRF 的 API 視圖。
它允許你用函數式視圖（Function-Based Views, FBV）定義 API 端點，而不是類式視圖（Class-Based Views, CBV）。 
它支持指定允許的 HTTP 方法（例如 GET, POST）並自動處理 DRF 的請求解析和響應格式化。
"""
from rest_framework.response import Response
"""
Response 是一個 DRF 提供的響應類，用於返回格式化的 API 響應（通常是 JSON 格式）。
它比 Django 的標準 HttpResponse 更適合 API 開發，因為它支持序列化數據、狀態碼和自動內容協商。
"""
# from django.http import Http404
from django.shortcuts import get_object_or_404
"""
get_object_or_404 是一個快捷函數，用於從資料庫查詢單個物件。
如果物件存在，則返回該物件；如果不存在，則自動引發 Http404 異常，Django 會將其渲染為 HTTP 404（Not Found）錯誤頁面或響應。
"""
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin)
#StaffEditorPermissionMixin 和 UserQuerySetMixin 是 Django 專用的工具，通常與 Django 的模型、視圖或 DRF 的 API 架構緊密整合。
#它們依賴 Django 的認證系統、ORM（物件關聯映射）或 DRF 的視圖類，無法獨立於 Django 環境使用。
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    """
    UserQuerySetMixin：
    功能：這是一個自定義的混入類（Mixin），通常用來過濾資料查詢（QuerySet），根據當前用戶的身份限制可見數據。
    作用：它可能會確保普通用戶只能看到自己的產品，而管理員（staff）可以看到所有產品。
    在我的程式碼中：UserQuerySetMixin 會修改 ProductListCreateAPIView 的 get_queryset 方法，根據用戶身份過濾產品數據。
    UserQuerySetMixin 自動過濾資料，確保用戶只看自己的東西。

    StaffEditorPermissionMixin：
    功能：這也是一個自定義混入類，用來檢查權限，確保只有特定用戶（例如管理員或編輯者）可以執行操作。
    作用：它可能會限制「創建」或「列出」產品的操作，只有具備管理員權限（staff）或特定權限的用戶才能訪問。
    在你的程式碼中：StaffEditorPermissionMixin 會為 ProductListCreateAPIView 添加權限檢查，確保非管理員無法操作。
    StaffEditorPermissionMixin 檢查權限，確保只有授權員工能動手改。

    generics.ListCreateAPIView：
    功能：這是 Django REST Framework 提供的一個通用視圖類，用於處理「列出」（List）和「創建」（Create）操作。
    視圖 (View) 是網頁應用裡負責處理用戶請求的「中間人」。
    用戶點擊或送資料時，視圖接收請求，決定怎麼處理(例如:列出或創建)，然後回傳結果 (如網頁、JSON)。
    作用：
    List：處理 GET 請求，返回產品列表（通常是 JSON 格式）。
    Create：處理 POST 請求，創建新產品並保存到資料庫。
    在你的程式碼中：ProductListCreateAPIView 繼承了 generics.ListCreateAPIView，所以它可以處理 /products/ 路徑的 GET（列出產品）和 POST（創建產品）請求。
    """
    queryset = Product.objects.all()
    """
    Product 是一個 Django 模型類，我在models.py自己定義的
    objects 是Product模型內的屬性，裡面包含所有搜尋結果。 
    .all()來源於Django 內建，來自 django.db.models.QuerySet(因為Product中的objects用到了class ProductQuerySet(models.QuerySet)，繼承了models.QuerySet)。
    """
    serializer_class = ProductSerializer
    """
    雖然這個類別中沒有呼叫到 serializer_class
    但其實generics.ListCreateAPIView內部有用到serializer_class
    所以serializer_class是一個在繼承generics.ListCreateAPIView的類別內一定要出現的東西
    或者是覆寫 get_serializer_class() 方法返回序列化器，但不常見
    """

    #serializer_class 的ProductSerializer裡面的rest_framework.serializers.ModelSerializer定義了模板，而 perform_create 中的 serializer 是使用這個模板創建的實際工具。
    def perform_create(self, serializer):
        """
        我的前端要有新增產品的功能，並在前端配置路由呼叫class ProductListCreateAPIView()才會觸發perform_create。
        但我現在前端沒有寫上創建產品的功能，我從admin新增產品不會觸發這段perform_create的功能(若沒寫contnet，自動把title的值填進content)
        """
        """
        perform_create(self, serializer) 是 Django REST Framework (DRF) 中用來自定義 POST 請求創建物件的邏輯，覆寫 generics.ListCreateAPIView 的預設行為。
        這段程式碼在創建 Product時因為繼承generics.ListCreateAPIView被觸發，確保新產品的 user 是當前登入用戶，並檢查 content 是否為空，若空則用 title 填補。serializer.save() 儲存最終資料。
        """
        """
        不覆寫 perform_create，DRF 預設只調用 serializer.save()，
        不會執行我的自定義邏輯 (title = serializer.validated_data.get('title'), content = serializer.validated_data.get('content') or None)
        導致 title 不會自動填充content， 可能用預設值或失敗。
        """
        """
        serializer不是自定義的變數，而是DRF提供的一個工具的原因:
        簡單來說就是因為有這行from .serializers import ProductSerializer
        而這行是在serializers.py匯入的，而serializers.py內有這行from rest_framework import serializers
        而serializers內有serializer，所以在這邊打上serializer才會有功能而不是自定義變數
        serializer 的功能來自 DRF 的視圖邏輯 (ListCreateAPIView 等)，它自動根據 serializer_class = ProductSerializer 生成 serializer 實例

        serializer 就像是一個翻譯器，主要負責：
        將 Python 物件（如 Django 模型）轉換為 JSON 數據（序列化）
        將 JSON 數據轉換為 Python 物件（反序列化）
        """
        title = serializer.validated_data.get('title')   #validated_data 是 serializer 的一個屬性，包含經過驗證的數據
        #validated_data功能:驗證資訊
        #validated_data來源:Django REST Framework，來自 rest_framework.serializers.Serializer。
        content = serializer.validated_data.get('content') or None   
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        #save和validated比較像，都是Django序列化器提供的方法，而get是python提供的方法

product_list_create_view = ProductListCreateAPIView.as_view()
"""
.as_view() 會回傳一個可調用的視圖函數（view function），這個函數會：
接收 HTTP 請求
根據請求方法執行相應的操作
返回 HTTP 響應

GET 請求響應：
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "第一個產品",
            "content": "產品描述",
            "price": 99.99
        },
        {
            "id": 2,
            "title": "第二個產品",
            "content": "產品描述",
            "price": 199.99
        }
    ]
}

POST 請求響應：
{
    "id": 3,
    "title": "新建的產品",
    "content": "新產品描述",
    "price": 299.99
}

所以，product_list_create_view 最終是一個功能完整的視圖函數，能夠：
處理 GET 和 POST 請求
自動進行權限檢查
處理數據序列化/反序列化
返回適當的 JSON 響應

視圖函數就是：
一個負責處理網頁請求的程式
像是網站的接待員
決定要給使用者什麼回應
確保請求被正確處理
"""

class ProductDetailAPIView(
    UserQuerySetMixin, 
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    """
    功能: generics.RetrieveAPIView 是 Django REST Framework (DRF) 提供的通用視圖類，用於處理查詢單一物件的 GET 請求，返回其詳細資料。
    來源: Django REST Framework，來自 rest_framework.generics。
    白話解釋: 這是一個「查詢工具」，專門用來處理 API 的 GET 請求，查找某個特定物件 (如某個產品)，然後把它的資料轉成 JSON 回傳。
    比如，訪問 /api/products/1/，它會返回 ID 為 1 的產品詳情。
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    """
    功能: generics.UpdateAPIView 是 Django REST Framework (DRF) 提供的通用視圖類，用於處理更新 (PUT/PATCH) 請求，更新現有模型實例。
    來源: Django REST Framework，來自 rest_framework.generics。
    白話解釋: 這是一個「更新工具」，專門用來處理 API 的更新請求。
    比如，發一個 PUT 請求到 /api/products/1/，它會找到 ID 為 1 的產品，更新它的資料 (如 title, price)，然後返回更新後的結果。
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    #這行沒用，只是標示一下

    #目前前端沒寫這個功能不觸發
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ## 

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    #這行沒用只是標示一下

    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

    # def post(): #HTTP -> post

product_mixin_view = ProductMixinView.as_view()

