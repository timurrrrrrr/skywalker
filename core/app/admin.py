from django.contrib import admin
from .models import CustomUser, Category, Product, CartItem

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
