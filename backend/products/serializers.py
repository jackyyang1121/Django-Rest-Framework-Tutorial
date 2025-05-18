from rest_framework import serializers
#功能: 導入 Django REST Framework (DRF) 的序列化模組，提供工具來定義序列化器，將模型資料轉為 JSON 或從 JSON 轉回模型。
from rest_framework.reverse import reverse
#功能: 導入 DRF 的 reverse 函數，用來生成 API 端點的 URL，根據視圖名稱和參數動態產生。
#像個「URL 導航」，幫你自動生成某個視圖的 URL (如 /api/products/1/)，不用手寫硬編碼路徑。
#我的 get_edit_url 用它來產生 product-edit 的 URL。
from api.serializers import UserPublicSerializer
#去api/serializers.py裡面找UserPublicSerializer

from .models import Product  #導入Product模型
from . import validators   #導入validators.py內自訂的驗證方法


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk',
            read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    """
    功能: source='user' 去Product.user找資料，再用UserPublicSerializer轉成JSON
    下面有class Meta，裡面有model = Product，所以source='user' 知道要去Product.user找資料
    來源: Django REST Framework，來自 rest_framework.serializers。
    白話解釋: source='user' 告訴 ProductSerializer，owner 欄位的資料要從 Product 模型的 user 屬性 (即 ForeignKey 欄位) 拿，然後用 UserPublicSerializer 序列化。
    就像說：「去 Product.user 找資料，再用 UserPublicSerializer 轉成 JSON。」
    """
    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
    # validate_title_no_hello: 禁止 title 含 "hello"，自訂於 validators.py。
    # unique_product_title: 確保 title 唯一，自訂於 validators.py。
    body = serializers.CharField(source='content')
    class Meta:
    #Meta 像是序列化器的「設定檔」，告訴 DRF 這個序列化器要處理哪個模型 (Product)，以及要把哪些欄位轉成 JSON。欄位列表 (fields) 可以包含模型欄位和自定義欄位。
        model = Product
        fields = [
            'owner',   #owner是使用者pk
            'pk',     #pk是隱藏的，不會顯示在json裡，但會在url裡顯示，這邊是產品的pk
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'endpoint',
        ]
        """
        Product 模型有：user, title, content, price, public。
        對應 ProductSerializer 的 fields:
        pk: 模型的隱式主鍵 (id)，自動包含。
        title, price, public: 直接映射Product模型欄位。
        body: 透過 serializers.CharField(source='content') 映射 content。
        owner: 透過 UserPublicSerializer 序列化 user 欄位。
        path, endpoint,sale_price: 自定義欄位，不直接對應模型欄位。
        """

    
    def get_edit_url(self, obj):
        #當 ProductSerializer 序列化 Product 物件時，DRF 會自動把正在處理的 Product 實例作為 obj 傳遞給這個方法
        request = self.context.get('request')
        """
        DRF 不直接綁定 request 給序列化器，而是透過 context 傳遞，保持靈活性。
        上下文傳遞: 在視圖 (如 ProductListCreateAPIView) 中，DRF 自動將 request 放進 context，傳給序列化器
        """
        """
        context 像個「資料袋」，DRF 在視圖 (如 ProductListCreateAPIView) 處理請求時，
        會把 request 之類的資訊裝進這個袋子，然後傳給序列化器 (ProductSerializer)。
        這樣序列化器就能用這些資訊 (如 request) 做事，比如生成 URL。
        """
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)   #kwargs是可以傳入動態參數例如dic而args是傳入位置參數例如tuple
    """
    這段程式碼想動態產生某個產品的編輯連結 (如 /api/products/1/update/)，讓前端可以直接拿到這個 URL，用來導向編輯頁面或發送更新請求。
    product-edit是為了配對urls.py裡的name='product-edit'
    配對urls.py裡的path('<int:pk>/update/', views.product_update_view, name='product-edit'),
    """
    """
    reverse("product-edit", kwargs={"pk": obj.pk}, request=request):
    reverse: DRF 的工具，生成名為 product-edit 的 URL。
    kwargs={"pk": obj.pk}: 傳入產品的 pk (主鍵，如 1)，用於 URL 動態參數。
    request=request: 確保 URL 包含正確的域名和路徑 (如 http://localhost:8000/api/products/1/update/)。
    reverse會先在urls.py裡找到 name='product-edit' 的路徑: /api/products/<int:pk>/update/，再填入填入 pk=1，生成 http://localhost:8000/api/products/1/update/
    """