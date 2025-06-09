from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    user_telegram_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Last name"))
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Telegram username"))
    phone_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Phone number"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")
