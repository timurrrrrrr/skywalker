from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('search/', views.ProductSearchView.as_view()),
    path('cart/add/', views.AddToCartView.as_view()),
]
