import pytest
from .models import Category, Product, Fridge
from datetime import datetime
from django.contrib.auth import get_user_model

# User = get_user_model()
# product_test = Product.objects.get(id=1)


@pytest.fixture()
def category_to_test():
    return Category.objects.create(
        name='fake name'
    )


@pytest.fixture()
def product_to_test():
    return Product.objects.create(
        name='fake product 200g',
        consumption_hours=5,
        default_price=5.00,
    )
    # Product.Category.add(['test'])


# @pytest.fixture()
# def product_fridge_to_test(product_test):
#     # user = User.objects.get(username='michalzolyniak')
#     return Fridge.objects.create(
#         product=product_test,
#         purchase_price=1.00,
#         date_added=datetime.now(),
#         open=True,
#         expiration_date=datetime.now()
#     )
#
