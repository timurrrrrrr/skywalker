from django.urls import path
from rest_framework import permissions
from rest_framework.schemas import get_schema_view, openapi

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="SkyWalker",
        default_version='v1',
        description="This site is for you",
        terms_of_service="https://www.skywalker.com/terms/",
        contact=openapi.Contact(email="djavarbekovt@gmail.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('search/', views.ProductSearchView.as_view()),
    path('cart/add/', views.AddToCartView.as_view()),
]
