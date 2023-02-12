from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

STATUS = (
    (1, "Eaten"),
    (2, "ejected"),
    (3, "fridge"),
)


class Category(models.Model):
    """
        product catgories
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class Fridge(models.Model):
    """
        Products in fridge per user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateTimeField()
    open = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, null=True)
    status_date = models.DateTimeField(null=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    """
        Product adds to fridge
    """
    name = models.CharField(max_length=100, unique=True)
    consumption_hours = models.IntegerField()
    category = models.ManyToManyField(Category)
    default_price = models.DecimalField(max_digits=5, decimal_places=2)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)


class Note(models.Model):
    """
        Note to product per user
    """
    # product = models.ForeignKey(Product, releted_name='notes', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return self.notes
