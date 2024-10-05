import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def model_factory():
    def factory(model, *args, **kwargs):
        return baker.make(model, *args, **kwargs)

    return factory


@pytest.fixture
@pytest.mark.django_db
def token(model_factory, client):
    user = model_factory(User)
    user.set_password('password')
    user.save()
    response = client.post('/api/v1/token/', data={'username': user.username, 'password': 'password'})
    return response.json().get('access')

@pytest.fixture
def authorized_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return client