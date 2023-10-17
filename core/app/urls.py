from django.urls import path
from drf_yasg import openapi
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
   Info(
      title="228",
      default_version='v1',
      description="Description of your API",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
