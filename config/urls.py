"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
from config import settings
from config.swagger import urlpatterns as doc_urls
from .views import TelegramTokenView

urlpatterns = doc_urls

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path("api/", include('user.urls')),
    path('api/telegram-token/', TelegramTokenView.as_view(), name='telegram_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", TemplateView.as_view(template_name="frontend/index.html")),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


