import pytest
from .models import Fridge, Product, Category
from django.contrib.auth import get_user_model
from datetime import datetime
import decimal
s = '23.456'
d = decimal.Decimal(s)

User = get_user_model()


# @pytest.mark.django_db
# def test_create_user_view(client):
#     data = {
#         'login': 'jakktos',
#         'password1': 'Sloneczna1!',
#         'password2': 'Sloneczna1!',
#         'email': 'michalzolyniak@o2.pl'
#     }
#     response = client.post('/add_user/', data)
#     assert response.status_code == 302, response.context['form'].errors
#     assert User.objects.get(username="jakktos")
#
#
# @pytest.mark.django_db
# def test_login_view(client):
#     data = {
#         'login': 'michalzolyniak',
#         'password': 'Sloneczna1!'
#     }
#     response = client.post('/login/', data)
#     assert response.status_code == 200, response.context['form'].errors
#
#
# @pytest.mark.django_db
# def test_add_category_view(client, category_to_test):
#     data = {
#         'name': 'fake name'}
#     response = client.post('/add_category/', data)
#     assert response.status_code == 302, response.context['form'].errors
#     assert Category.objects.get(name="fake name")
#
#
# @pytest.mark.django_db
# def test_add_product_view(client, product_to_test):
#     data = {
#         'name': 'fake product 200g',
#         'consumption_hours': 5,
#         'default_price': 5.00,
#     }
#     response = client.post('/add_product/', data)
#     assert response.status_code == 302, response.context['form'].errors
#     assert Product.objects.get(name="fake product 200g")


@pytest.mark.django_db
def test_add_product_to_fridge_view(client):
    name = 'fake product 200g',
    product_test = Product.objects.create(
        name=name,
        consumption_hours=5,
        default_price=5.00,
    )
    date_added = datetime.now()
    data = {
        'product': product_test.id,
        'purchase_price': 23,
        'date_added': date_added,
        'open': False,
        'expiration_date': datetime.now()
    }

    response = client.post('/add_product_to_fridge/', data)
    assert response.status_code == 302, response.context['form'].errors
    assert Fridge.objects.get(date_added=date_added)