from .models import Category, Product, ProductHistory, Order, OrderItem
from django.db import transaction
from rest_framework import serializers
from shop.management.commands.runbot import send_telegram_message

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = GetProductSerializer(instance.category).data
        return rep

class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = '__all__'

class GetProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'sku']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = GetProductSerializer(instance.product).data
        return rep

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    @transaction.atomic
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status')
        if old_status != 'bekor qilindi' and new_status == 'bekor qilindi':
            for order_item in instance.order_items.all():
                product = order_item.product
                product.count += order_item.quantity
                product.save(update_fields=["count"])
        return super().update(instance, validated_data)

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

        user = order.user
        if user.user_telegram_id:
            items = order.order_items.all()
            items_text = "\n".join(
                [f"📌 {item.product.name} - {item.quantity} dona" for item in items]
            )

            msg = (
                f"🔥 <b>Yangi buyurtma!</b>\n"
                f"👤 <b>Foydalanuvchi:</b> {user.first_name}\n"
                f"📞 <b>Telefon raqami:</b> {user.phone_number}\n"
                f"📦 <b>Status:</b> {order.status}\n"
                f"💰 <b>Umumiy narx:</b> {order.total_price} USD\n"
                f"🧾 <b>Buyurtma ID:</b> {order.id}\n"
                f"\n<b>Mahsulotlar:</b>\n{items_text}"
            )
            send_telegram_message(msg)

        return order
