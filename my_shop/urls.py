from django.urls import path
from shop import settings

from .views import MainView, ProductListView, ProductDetail
from .views import choose_sex, product_redirect_view

urlpatterns = [
    path('', MainView.as_view(), name='main-page'),
    path('products/', choose_sex, name='choose-sex'),
    path('products/detail/<slug:product_slug>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<slug:sex>/', product_redirect_view, name='products'),
    path('products/<slug:sex>/<slug:category>/', ProductListView.as_view(), name='product-list'),
]
