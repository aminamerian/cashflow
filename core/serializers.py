from rest_framework import serializers
from datetime import datetime
from core.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'date']

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class MonthlySummarySerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()
    amount = serializers.IntegerField(source='total_amount')

    @staticmethod
    def get_date(obj):
        return datetime.strptime(str(obj['date__month']), "%m").strftime("%B")


class CategoryReportSerializer(serializers.Serializer):
    category = serializers.CharField(source='category__name')
    amount = serializers.IntegerField(source='total_amount')
