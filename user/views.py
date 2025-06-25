from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum, ExpressionWrapper, F, FloatField
from rest_framework.views import APIView

from shop.models import Order, Product
from shop.pagination import TenItemPagination
from .models import User
from .serialazers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = TenItemPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'id']
    ordering = ['-created_at']
    search_fields = ('first_name', 'phone_number')

    def list(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(self.get_queryset())  # <- sahifalash

        user_data = []
        for user in queryset:
            orders = Order.objects.filter(user=user, status='tasdiqlandi')
            orders_count = orders.count()
            orders_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

            user_data.append({
                "user_id": user.id,
                "first_name": user.first_name,
                "phone_number": user.phone_number,
                "orders_count": orders_count,
                "orders_amount": orders_amount,
            })

        return self.get_paginated_response(user_data)


class UserStatisticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all().count()
        orders = Order.objects.all()
        products = Product.objects.all()
        product_type_count = products.count()
        product_count = products.aggregate(Sum('count'))['count__sum'] or 0
        product_total_amount = products.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('price') * F('count'),
                    output_field=FloatField()
                )
            )
        )['total'] or 0
        product_total_amount_approved = products.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('price_received') * F('count'),
                    output_field=FloatField()
                )
            )
        )['total'] or 0
        orders_count_approved = orders.filter(status='tasdiqlandi').count()
        orders_count_in_process = orders.filter(status='jarayonda').count()
        orders_count_canceled = orders.filter(status='bekor qilindi').count()
        orders_amount = orders.filter(status='tasdiqlandi').aggregate(Sum('total_price'))['total_price__sum'] or 0
        product_total_net_profit = product_total_amount - product_total_amount_approved

        orders = Order.objects.filter(status='tasdiqlandi').prefetch_related('order_items__product')
        orders_amount_approved = 0
        for order in orders:
            for item in order.order_items.all():
                if item.product and item.product.price_received and item.quantity:
                    orders_amount_approved += item.product.price_received * item.quantity
        net_profit = orders_amount - orders_amount_approved
        results = {
            "user_count": users,
            "product_type_count": product_type_count,
            "product_count": product_count,
            "product_total_amount": product_total_amount,
            "product_total_amount_approved": product_total_amount_approved,
            "product_total_net_profit": product_total_net_profit,
            "orders_count_approved": orders_count_approved,
            "orders_count_in_process": orders_count_in_process,
            "orders_count_canceled": orders_count_canceled,
            "orders_amount": orders_amount,
            "orders_amount_approved": orders_amount_approved,
            "net_profit": net_profit,

        }

        return Response(results)
