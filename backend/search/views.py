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
           user = request.user.username   #request.user可以直接使用，並抓到User物件內的資訊，User是Django預設使用者模型包含id、username、password、email等資訊
           #不管User是用預設模型還是自訂模型，只要在settings.py裡有AUTH_USER_MODEL，就可以用request.user來抓到User物件
        query = request.GET.get('q')    #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的q，也就是searchParams中的q，q在index.html中的search表單中有定義name="q"，也就是這邊存取的是我在表單打的字
        public = str(request.GET.get('public')) != "0"   
        #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的public，也就是searchParams中的public，但是目前insex.html搜尋表單內我並沒有添加public這個參數所以目前?${searchParams}中沒有存取到public這個參數，回傳預設值True
        tag = request.GET.get('tag') or None    #這邊去拿 `${baseEndpoint}/search/?${searchParams}`中的tag，也就是searchParams中的tag，但是目前insex.html搜尋表單內我並沒有添加tag這個參數所以目前?${searchParams}中沒有存取到tag這個參數
        #因為我前端index.html搜尋表單內沒有添加name=tag和name=public這兩個參數，所以這邊的tag和public會是None，因為?${searchParams}沒辦法存取到這兩個參數
        if not query:
            return Response('', status=400)   #一開始還沒在瀏覽器上打字所以query是空的，這邊就會先回傳一次400錯誤
        results = client.perform_search(query, tags=tag, user=user, public=public)  #其實目前只有query和user有值，tag和public是None和預設值True
        return Response(results) #回傳API的結果，包含搜尋結果

