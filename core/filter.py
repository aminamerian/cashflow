from django_filters import rest_framework as filters

from core.models import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'amount': ['exact', 'lte', 'gte'],
            'type': ['exact'],
            'category': ['exact'],
            'date': ['exact', 'lte', 'gte'],
        }
