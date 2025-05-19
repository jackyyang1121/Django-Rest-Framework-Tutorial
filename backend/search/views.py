from rest_framework import generics   
from rest_framework.response import Response   

from products.models import Product
from products.serializers import ProductSerializer

from . import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:     
        # 確認用戶已登入，is_authenticated 是 request.user 的屬性。
        # request.user 是由 django.contrib.auth.middleware.AuthenticationMiddleware 中介層自動加到每個 HttpRequest 物件上的。
        # 只要 settings.py 的 MIDDLEWARE 裡有 'django.contrib.auth.middleware.AuthenticationMiddleware'，           
        # 我在任何 view 裡都可以安全地使用 request.user 和 request.user.is_authenticated。
           user = request.user.username   #request.user可以直接使用，並抓到User物件內的資訊，User包含id、username、password、email等資訊
           #不管User是用預設模型還是自訂模型，只要在settings.py裡有AUTH_USER_MODEL，就可以用request.user來抓到User物件
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