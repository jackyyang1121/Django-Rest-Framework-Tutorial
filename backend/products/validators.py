from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product

#只是過濾不要讓產品title有hello
def validate_title_no_hello(value):
    if "hello" in value.lower():
        raise serializers.ValidationError(f"{value} is not allowed")
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')