from django.test import TestCase
import pytest
from .models import Fridge, Product, Category
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_add_category_view(client):
    data = {
        'name': 'testwwwwww',
    }
    response = client.post('/add_category/', data)
    # assert response.status_code == 302 # redirect to anatoher page
    assert Category.objects.get(name='test'),response.context['form'].errors

@pytest.mark.django_db
def test_add_create_user_view(client):
    data = {
        'login': 'jakktos',
        'password1': 'Sloneczna1!',
        'password2': 'Sloneczna1!',
        'email': 'michalzolyniak@o2.pl'
    }
    response = client.post('/add_user/', data)
    assert response.status_code == 302, response.context['form'].errors
    assert User.objects.get(username="jakktos")


@pytest.mark.django_db
def test_with_authenticated_client(client):
    username = "michalzolyniak"
    password = "Sloneczna1!"
    user = User.objects.create_user(username=username, password=password)
    client.force_login(user)
    response = client.get('/')
    assert response.status_code == 200