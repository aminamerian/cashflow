from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='transactions')
    amount = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey('TransactionCategory', on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"


class TransactionCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Balance(models.Model):
    amount = models.BigIntegerField(default=0)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='balance')

    def __str__(self):
        return f"{self.user} -> {self.amount}"
