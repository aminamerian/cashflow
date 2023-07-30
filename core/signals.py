from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Balance


@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, **kwargs):
    total_amount = Transaction.objects.filter(user=instance.user).aggregate(total=Sum('amount'))['total']
    if total_amount is None:
        total_amount = 0

    balance, _ = Balance.objects.get_or_create(user=instance.user)
    balance.amount = total_amount
    balance.save()
