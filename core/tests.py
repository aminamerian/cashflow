import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
from .models import Transaction
from .views import TransactionViewSet, MonthlySummaryReport, CategoryReport
from unittest.mock import patch, MagicMock


def test_transaction_list_authenticated(factory, user, transaction, transaction2):
    view = TransactionViewSet.as_view({'get': 'list'})
    url = reverse('core:transaction-list')

    request = factory.get(url)
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


def test_transaction_list_unauthenticated(factory):
    view = TransactionViewSet.as_view({'get': 'list'})
    url = reverse('core:transaction-list')
    request = factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_transaction_create_authenticated(factory, user, salary_category):
    data = {
        "amount": 200,
        "type": "income",
        "category": salary_category.id,
        "date": "2023-07-10",
    }
    view = TransactionViewSet.as_view({'post': 'create'})
    url = reverse('core:transaction-list')
    request = factory.post(url, data=json.dumps(data), content_type='application/json')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED


def test_transaction_update_authenticated(factory, user, transaction, salary_category):
    updated_data = {
        "amount": 300,
        "type": "expense",
        "category": salary_category.id,
        "date": "2023-07-15",
    }
    view = TransactionViewSet.as_view({'put': 'update'})
    url = reverse('core:transaction-detail', args=[transaction.id])
    request = factory.put(url, data=json.dumps(updated_data), content_type='application/json')
    force_authenticate(request, user=user)
    response = view(request, pk=transaction.id)
    assert response.status_code == status.HTTP_200_OK
    assert Transaction.objects.filter(user=user, amount=300, type='expense', category=salary_category,
                                      date='2023-07-15').exists()


def test_transaction_retrieve_authenticated(factory, user, transaction, salary_category):
    view = TransactionViewSet.as_view({'get': 'retrieve'})
    url = reverse('core:transaction-detail', args=[transaction.id])
    request = factory.get(url)
    force_authenticate(request, user=user)
    response = view(request, pk=transaction.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == 100


def test_transaction_delete_authenticated(factory, user, transaction):
    view = TransactionViewSet.as_view({'delete': 'destroy'})
    url = reverse('core:transaction-detail', args=[transaction.id])
    request = factory.delete(url)
    force_authenticate(request, user=user)
    response = view(request, pk=transaction.id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Transaction.objects.filter(id=transaction.id).exists()


def test_monthly_summary_report_view(factory, user):
    url = reverse('core:monthly-summary-report')
    request = factory.get(url)
    factory.user = user
    queryset_mock = MagicMock()
    queryset_mock.return_value.values.return_value.annotate.return_value = [
        {'date__month': 1, 'total_amount': 100},
        {'date__month': 2, 'total_amount': 200},
        {'date__month': 3, 'total_amount': 300}
    ]
    with patch('core.views.Transaction.objects.filter', queryset_mock), \
            patch('core.views.MonthlySummarySerializer') as serializer_mock:
        serializer_mock.return_value.data = queryset_mock.return_value.values.return_value.annotate.return_value
        response = MonthlySummaryReport.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {'date__month': 1, 'total_amount': 100},
        {'date__month': 2, 'total_amount': 200},
        {'date__month': 3, 'total_amount': 300}
    ]


def test_category_report_view(factory, user):
    url = reverse('core:category-report')
    request = factory.get(url)
    factory.user = user
    queryset_mock = MagicMock()
    queryset_mock.return_value.values.return_value.annotate.return_value = [
        {'category__name': 'Category A', 'total_amount': 500},
        {'category__name': 'Category B', 'total_amount': 300},
        {'category__name': 'Category C', 'total_amount': 200}
    ]
    with patch('core.views.Transaction.objects.filter', queryset_mock), \
            patch('core.views.CategoryReportSerializer') as serializer_mock:
        serializer_mock.return_value.data = queryset_mock.return_value.values.return_value.annotate.return_value
        response = CategoryReport.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {'category__name': 'Category A', 'total_amount': 500},
        {'category__name': 'Category B', 'total_amount': 300},
        {'category__name': 'Category C', 'total_amount': 200}
    ]
