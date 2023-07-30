import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from core.models import Transaction, TransactionCategory


@pytest.fixture(scope='module')
def factory():
    return APIRequestFactory()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="test_password")


@pytest.fixture
def salary_category(db):
    return TransactionCategory.objects.create(
        name='salary'
    )


@pytest.fixture
def bonus_category(db):
    return TransactionCategory.objects.create(
        name='bonus'
    )


@pytest.fixture
def transaction(user, salary_category):
    transaction = Transaction.objects.create(
        user=user,
        amount=100,
        type='income',
        category=salary_category,
        date='2023-07-01'
    )
    return transaction


@pytest.fixture
def transaction2(user, bonus_category):
    transaction = Transaction.objects.create(
        user=user,
        amount=-1000,
        type='expense',
        category=bonus_category,
        date='2023-07-28'
    )
    return transaction
