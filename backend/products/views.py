from rest_framework import generics, mixins
"""
generics 模組提供了一組通用視圖類（Generic Views），用於快速構建常見的 API 端點，例如列表、創建、檢索、更新或刪除資源（CRUD 操作）。 
例如：
generics.ListAPIView：用於顯示資源列表。
generics.CreateAPIView：用於創建新資源。
generics.RetrieveUpdateDestroyAPIView：用於檢索、更新或刪除單個資源。

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
    在你的程式碼中：UserQuerySetMixin 會修改 ProductListCreateAPIView 的 get_queryset 方法，根據用戶身份過濾產品數據。

    StaffEditorPermissionMixin：
    功能：這也是一個自定義混入類，用來檢查權限，確保只有特定用戶（例如管理員或編輯者）可以執行操作。
    作用：它可能會限制「創建」或「列出」產品的操作，只有具備管理員權限（staff）或特定權限的用戶才能訪問。
    在你的程式碼中：StaffEditorPermissionMixin 會為 ProductListCreateAPIView 添加權限檢查，確保非管理員無法操作。

    generics.ListCreateAPIView：
    功能：這是 Django REST Framework 提供的一個通用視圖類，用於處理「列出」（List）和「創建」（Create）操作。
    作用：
    List：處理 GET 請求，返回產品列表（通常是 JSON 格式）。
    Create：處理 POST 請求，創建新產品並保存到資料庫。
    在你的程式碼中：ProductListCreateAPIView 繼承了 generics.ListCreateAPIView，所以它可以處理 /products/ 路徑的 GET（列出產品）和 POST（創建產品）請求。
    """
    queryset = Product.objects.all()
    """
    Product 是一個 Django 模型類，我在models.py自己定義的
    是 Django 自動為每個模型提供的（除非我自訂了管理器）。
    all() 是 objects 管理器的一個方法，用來返回資料庫中所有的 Product 記錄（一個 QuerySet，一個Django的型別）。
    """
    serializer_class = ProductSerializer
    """
    雖然這個類別中沒有呼叫到 serializer_class
    但其實generics.ListCreateAPIView內部有用到serializer_class
    所以serializer_class是一個在繼承generics.ListCreateAPIView的類別內一定要出現的東西
    """
    """
    A[rest_framework.serializers 模組] -->|提供| B[Serializer 基礎類]
    B -->|繼承| C[serializers.ModelSerializer]
    C -->|繼承| D[ProductSerializer]
    D -->|實例化| E[serializer 物件]
    """

    def perform_create(self, serializer):
        """
        簡單來說就是因為有這行from .serializers import ProductSerializer
        而這行是在serializers.py匯入的，而serializers.py內有這行from rest_framework import serializers
        而serializers內有serializer，所以在這邊打上serializer才會有功能而不是自定義變數

        serializer 就像是一個翻譯器，主要負責：
        將 Python 物件（如 Django 模型）轉換為 JSON 數據（序列化）
        將 JSON 數據轉換為 Python 物件（反序列化）
        """
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')   #validated_data 是 serializer 的一個屬性，包含經過驗證的數據
        content = serializer.validated_data.get('content') or None   
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        # send a Django signal

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(
    UserQuerySetMixin, 
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk' ??

product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

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

    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#     '''
#     Not gonna use this method
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# product_list_view = ProductListAPIView.as_view()


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

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method  

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all() 
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)
