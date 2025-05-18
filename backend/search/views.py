from rest_framework import generics
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

from . import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:     #確認用戶已登入，is_authenticated來自request.user的功能，request.user是django.contrib.auth.middleware.AuthenticationMiddleware 中介層自動附加到每個 HttpRequest 物件的。
            #settings.py 中有MIDDLEWARE 設定
            #MIDDLEWARE = [
            #     ...
            #     'django.contrib.auth.middleware.AuthenticationMiddleware',
            #     ...
            # ]
            #所以每個檔案都可以使用request.user
           user = request.user.username
        query = request.GET.get('q')    #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的q，也就是searchParams中的q
        public = str(request.GET.get('public')) != "0"   #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的public，也就是searchParams中的public
        tag = request.GET.get('tag') or None    #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的tag，也就是searchParams中的tag
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, tags=tag, user=user, public=public)
        return Response(results)

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results