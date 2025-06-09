from django.contrib import admin
from shop.models import Category, Product, ProductHistory, Order, OrderItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductHistory)
admin.site.register(Order)
admin.site.register(OrderItem)
