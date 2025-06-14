from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.views import APIView

from shop.models import Order, Product
from .models import User
from .serialazers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_data = []

        for user in queryset:
            orders = Order.objects.filter(user=user, status='tasdiqlandi  ')
            orders_count = orders.count()
            orders_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

            user_data.append({
                "user_id": user.id,
                "first_name": user.first_name,
                "phone_number": user.phone_number,
                "orders_count": orders_count,
                "orders_amount": orders_amount,
            })

        return Response(user_data)


class UserStatisticsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().count()
        orders = Order.objects.filter(status='tasdiqlandi')
        products = Product.objects.all().count()
        orders_count = orders.count()
        orders_amount = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        results = {
            "user_count": users,
            "product_count": products,
            "orders_count": orders_count,
            "orders_amount": orders_amount,
        }

        return Response(results)
