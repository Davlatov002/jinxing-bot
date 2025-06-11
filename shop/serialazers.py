from .models import Category, Product, ProductHistory, Order, OrderItem
from django.db import transaction
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("order_items")
        if not items_data:
            raise serializers.ValidationError("No items")
        for item in items_data:
            product = item["product"]
            if item["quantity"] > product.count:
                raise serializers.ValidationError(
                    f"Mahsulot «{product.name}» uchun omborda yetarli miqdor yo‘q."
                )
        order = Order.objects.create(**validated_data)

        total = 0
        order_items = []
        for item in items_data:
            product  = item["product"]
            quantity = item["quantity"]
            product.count -= quantity
            product.save(update_fields=["count"])
            order_item = OrderItem.objects.create(
                product  = product,
                quantity = quantity,
                price    = product.price * quantity,
            )
            order_items.append(order_item)
            total += product.price * quantity
        order.order_items.set(order_items)
        order.total_price = total
        order.save()

        return order
