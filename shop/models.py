from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Client(models.Model):
    name = models.CharField('Name', max_length=50)
    email = models.EmailField('Email', max_length=150)
    phone_number = models.IntegerField('Phone number', blank=True, null=True)
    address = models.TextField('Address', blank=True, null=True)
    registered = models.DateTimeField('Registered', auto_now_add=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('-registered',)

    def __str__(self) -> str:
        return f'{self.name}, {self.email}, {self.phone_number}'


class Product(models.Model):
    name = models.CharField('Name', max_length=50)
    description = models.TextField('Description')
    price = models.DecimalField(
        'Price', max_digits=8, decimal_places=2,
        validators=[MinValueValidator(limit_value=Decimal(0.1))])
    count = models.PositiveIntegerField('Number of products', default=1)
    image = models.ImageField(upload_to='images/')
    added = models.DateTimeField('Product added', auto_now_add=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-added',)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(
        Client, verbose_name='client', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        'Product', verbose_name='Products')
    total_amount = models.DecimalField(
        'Total amount', max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField('Created', auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'{self.client}, {self.total_amount}, {self.created}'