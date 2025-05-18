from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk',
            read_only=True
    )
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    #Serializer 是序列化器，負責將模型資料轉換為 JSON 格式。
    username = serializers.CharField(read_only=True)
    #read_only=True 表示這個欄位是只讀的，不能在序列化過程中被修改。
    this_is_not_real = serializers.CharField(read_only=True)
    #CharField 功能是我給他Python他就轉JSON資料，我給他JSON他轉Python資料，且負責處理文字
    id = serializers.IntegerField(read_only=True)
    #IntegerField 功能是我給他Python他就轉JSON資料，我給他JSON他轉Python資料，且負責處理整數
    #這邊是使用者pk
