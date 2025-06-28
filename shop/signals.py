from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product, ProductHistory

previous_counts = {}

@receiver(pre_save, sender=Product)
def cache_previous_count(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = Product.objects.get(pk=instance.pk)
            previous_counts[instance.pk] = previous_instance.count
        except Product.DoesNotExist:
            previous_counts[instance.pk] = None

@receiver(post_save, sender=Product)
def create_history_on_create_or_update(sender, instance, created, **kwargs):
    if created:
        ProductHistory.objects.create(
            name=instance.name,
            price=instance.price,
            price_received=instance.price_received,
            category=instance.category.name if instance.category else None,
            count=instance.count,
            sku=instance.sku,
            status=ProductHistory.Status.YARATILDI
        )
    else:
        previous_count = previous_counts.get(instance.pk)
        if previous_count is not None and previous_count != instance.count:
            count_difference = instance.count - previous_count
            if count_difference > 0:
                status = ProductHistory.Status.QOSHILDI
            else:
                status = ProductHistory.Status.AYRILDI

            ProductHistory.objects.create(
                name=instance.name,
                price=instance.price,
                price_received=instance.price_received,
                category=instance.category.name if instance.category else None,
                count=count_difference,
                sku=instance.sku,
                status=status
            )

    previous_counts.pop(instance.pk, None)
