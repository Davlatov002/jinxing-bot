
from rest_framework import viewsets
from .models import Category, Product, Order, OrderItem, ProductHistory
from .serialazers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, ProductHistorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ProductHistoryViewSet(viewsets.ModelViewSet):
    queryset = ProductHistory.objects.all()
    serializer_class = ProductHistorySerializer