import json
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .serializers import UserSerializer
from .views import UserViewSet


def test_register_valid_user(factory, db):
    data = {
        "username": "testuser",
        "password": "testpassword",
    }
    view = UserViewSet.as_view({'post': 'register'})
    url = reverse('accounts:users-register')
    request = factory.post(url, data=json.dumps(data), content_type='application/json')
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.filter(username="testuser").exists()
    assert response.data == UserSerializer(get_user_model().objects.get(username="testuser")).data


def test_register_invalid_data(factory, db):
    data = {
        "username": "testuser",
    }
    view = UserViewSet.as_view({'post': 'register'})
    url = reverse('accounts:users-register')
    request = factory.post(url, data=json.dumps(data), content_type='application/json')
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_duplicate_username(factory, db):
    data = {
        "username": "existinguser",
        "password": "testpassword",
    }
    view = UserViewSet.as_view({'post': 'register'})
    url = reverse('accounts:users-register')

    request = factory.post(url, data=json.dumps(data), content_type='application/json')
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED

    request = factory.post(url, data=json.dumps(data), content_type='application/json')
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_multiple_users(factory, db):
    data_user1 = {
        "username": "user1",
        "password": "password1",
    }
    data_user2 = {
        "username": "user2",
        "password": "password2",
    }
    view = UserViewSet.as_view({'post': 'register'})
    url = reverse('accounts:users-register')
    request_user1 = factory.post(url, data=json.dumps(data_user1), content_type='application/json')
    request_user2 = factory.post(url, data=json.dumps(data_user2), content_type='application/json')

    response_user1 = view(request_user1)
    response_user2 = view(request_user2)

    assert response_user1.status_code == status.HTTP_201_CREATED
    assert response_user2.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.filter(username="user1").exists()
    assert get_user_model().objects.filter(username="user2").exists()
