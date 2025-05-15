from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin)

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



################################讀到這裡############################################



    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        # send a Django signal
    
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user)


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
