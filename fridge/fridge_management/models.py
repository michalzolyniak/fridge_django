from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    consumption_date_close = models.DateField()
    consumption_hours = models.IntegerField()
    category = models.ManyToManyField(Category)
    default_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Fridge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateTimeField()
    open = models.BooleanField(default=False)


class Note(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField()
