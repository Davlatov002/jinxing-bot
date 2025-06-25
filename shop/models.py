from django.utils.translation import gettext_lazy as _
from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Category name"))
    image = models.ImageField(upload_to="category/", blank=True, null=True, verbose_name=_("Image"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Bo'lim")
        verbose_name_plural = _("Bo'limlar")


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Product name"))
    price = models.FloatField(blank=True, null=True, verbose_name=_("Product price"))
    price_received = models.FloatField(blank=True, null=True, verbose_name=_("Product price received"))
    sku = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Product SKU"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Product description"))
    count = models.IntegerField(blank=True, null=True, verbose_name=_("Product count"))
    image = models.ImageField(upload_to="product/", blank=True, null=True, verbose_name=_("Image"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Product category"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Maxsulot")
        verbose_name_plural = _("Maxsulotlar")


class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    count = models.IntegerField(blank=True, null=True, verbose_name=_("Product count"))
    price = models.FloatField(blank=True, null=True, verbose_name=_("Product price"))
    sku = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Product SKU"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.IntegerField(blank=True, null=True, verbose_name=_("Product quantity"))
    price = models.FloatField(blank=True, null=True, verbose_name=_("Product price"))


class Order(models.Model):
    class Status(models.TextChoices):
        JARAYONDA = 'jarayonda', _('Jarayonda')
        TASDIQLANDI = 'tasdiqlandi', _('Tasdiqlandi')
        BEKOR_QILINDI = 'bekor qilindi', _('Bekor qilindi')

    total_price = models.FloatField(blank=True, null=True, verbose_name=_("Total price"))
    order_items = models.ManyToManyField(OrderItem, verbose_name=_("Order items"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.JARAYONDA,
        verbose_name=_("Status")
    )