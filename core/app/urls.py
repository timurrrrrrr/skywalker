from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('products/', views.ProductList.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('products/<int:product_id>/', views.product_detail),
]
