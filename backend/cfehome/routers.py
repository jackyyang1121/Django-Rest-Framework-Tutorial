from rest_framework.routers import DefaultRouter


from products.viewsets import ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductGenericViewSet, basename='products')  #這行的功用是讓products/urls.py的urlpatterns可以配對到
urlpatterns = router.urls