from rest_framework import serializers
#功能: 導入 Django REST Framework (DRF) 的序列化模組，提供工具來定義序列化器，將模型資料轉為 JSON 或從 JSON 轉回模型。
from rest_framework.reverse import reverse
#功能: 導入 DRF 的 reverse 函數，用來生成 API 端點的 URL，根據視圖名稱和參數動態產生。
#像個「URL 導航」，幫你自動生成某個視圖的 URL (如 /api/products/1/)，不用手寫硬編碼路徑。
#我的 get_edit_url 用它來產生 product-edit 的 URL。
from api.serializers import UserPublicSerializer
#去api/serializers.py裡面找UserPublicSerializer

from .models import Product
from . import validators


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk',
            read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    
    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
    body = serializers.CharField(source='content')
    class Meta:
        model = Product
        fields = [
            'owner',
            'pk',
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'endpoint',
        ]
    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }
    
    def get_edit_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request) 
