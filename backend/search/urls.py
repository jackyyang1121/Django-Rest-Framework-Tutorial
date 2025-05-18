from django.urls import path

from . import views

# localhost:8000/api/search/
urlpatterns = [
    path('', views.SearchListView.as_view(), name='search')
]