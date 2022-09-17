import pytest
from .models import Category



@pytest.fixture()
def category():
    return Category.objects.create(
        name='fake name'
    )

# @pytest.fixture()
# def products():
#     product1 = Product.objects.create(
#         name='fake name',
#         description='fake description',
#         price=22,
#     )
#     product2 = Product.objects.create(
#         name="schabowy",
#         description="wspaniały",
#         price=20,
#     )
#     product3 = Product.objects.create(
#         name="arbuz",
#         description='zielony',
#         price=12,
#     )
#     return product1, product2, product3
