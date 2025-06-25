from django.contrib import admin
from shop.models import Category, Product, ProductHistory, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'total_price', 'status', 'created_at')

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = 'User First Name'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductHistory)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
