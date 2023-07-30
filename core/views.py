from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.models import Transaction
from core.serializers import TransactionSerializer, MonthlySummarySerializer, CategoryReportSerializer
from core.filter import TransactionFilter


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['amount', 'type', 'category', 'date']
    ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def get_serializer_class(self):
        return TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MonthlySummaryReport(APIView):
    def get(self, request):
        user = request.user
        queryset = Transaction.objects.filter(user=user).values('date__month').annotate(total_amount=Sum('amount'))
        serializer = MonthlySummarySerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryReport(APIView):
    def get(self, request):
        user = request.user
        queryset = Transaction.objects.filter(user=user).values('category__name').annotate(total_amount=Sum('amount'))
        serializer = CategoryReportSerializer(queryset, many=True)
        return Response(serializer.data)
