from django.contrib import admin
from shop.models import Category, Product, ProductHistory, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'total_price', 'status', 'created_at')
    search_fields = ('user_first_name', 'total_price', 'status')
    list_filter = ('status',)

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = 'User First Name'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'count', 'category', 'created_at')
    search_fields = ('name', 'sku')
    list_filter = ('category',)

class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'count', 'category', 'status', 'created_at')
    search_fields = ('name', 'sku')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductHistory, ProductHistoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
