from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('products/', views.product_list, name='product-list'),
    path('brands/', views.brand_list, name='brand-list'),
    path('products/<int:product_id>/', views.product_detail, name='product-detail'),
]
