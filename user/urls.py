from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserStatisticsAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', UserStatisticsAPIView.as_view(), name='user-statistics'),
]