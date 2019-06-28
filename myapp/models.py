from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=20, blank=False, default='Windsor')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100

class Client(User):
    PROVINCE_CHOICES = [ ('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.username

class Order(models.Model):
    ORDERSTATUS_CHOICES = [(0,'Order Cancelled'),(1, 'Order Placed'),(2, 'Order Shipped'),(3, 'Order Delivered')]
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #because it's FK, if delete, cascade delete
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=1)
    order_status = models.IntegerField(choices=ORDERSTATUS_CHOICES, default=1)
    status_date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return "For %d %s  by %s" % (self.num_units, self.product, self.client)

    def totoal_cost(self):
        total = 0.00
        total = self.num_units * self.product.price
        return "Totoal cost: %d" % (total)