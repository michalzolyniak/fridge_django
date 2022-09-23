import pytest
from .models import Fridge, Product, Category
from django.test import Client
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


@pytest.mark.django_db
def test_create_user_view(client):
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
def test_login_view(client):
    data = {
        'login': 'michalzolyniak',
        'password': 'Sloneczna1!'
    }
    response = client.post('/login/', data)
    assert response.status_code == 200, response.context['form'].errors


# @pytest.mark.django_db
# def test_with_authenticated_client(client):
#     username = "michalzolyniak"
#     password = "Sloneczna1!"
#     user = User.objects.create_user(username=username, password=password)
#     client.force_login(user)
#     response = client.get('/')
#     assert response.status_code == 200


@pytest.mark.django_db
def test_add_category_view(client, category_to_test):
    assert Category.objects.get(name="fake name")


@pytest.mark.django_db
def test_add_product_view(client, product_to_test):
    assert Product.objects.get(name="fake product 200g")

# @pytest.mark.django_db
# def test_add_product_to_fridge_view(client):
#     # user = User.objects.get(username='michalzolyniak')
#     # product_test = Product.objects.get(id=6)
#     # breakpoint()
#     # data = {
#     #     'product': product_test,
#     #     'purchase_price': 1.00,
#     #     'expiration_date': datetime.now(),
#     #     'date_added': datetime.now(),
#     #     'open': True,
#     # }
#     # response = client.post('/add_product_to_fridge/', data)
#     assert Fridge.objects.get(purchase_price=8.00)
