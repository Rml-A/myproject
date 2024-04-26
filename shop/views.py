from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .forms import ProductForm
from .models import Client, Order, Product


def index(request):
    return render(request, 'index.html', context={
        'products': Product.objects.all()
    })


def get_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})


def get_client(request, pk):
    client = Client.objects.filter(pk=pk)
    return HttpResponse(client)


def delete_client(request, pk):
    Client.objects.filter(pk=pk).delete()
    return HttpResponse('Client Deleted!')


def order(request, pk):
    client = get_object_or_404(Client, pk=pk)
    orders = Order.objects.filter(client=client).order_by('-created')
    prod_dict = {}
    for order in orders:
        products = order.products.filter(order=order.pk)
        product_set = set()
        for product in products:
            product_set.add(product.name)
        prod_dict[order.pk] = product_set
    return render(request, 'order.html', {
        'client': client, 'orders': orders,
        'products': prod_dict})


def client_products(request, pk: int, days: int):
    product_set = set()
    now = timezone.now()
    before = now - timedelta(days=days)
    client = get_object_or_404(Client, pk=pk)
    orders = Order.objects.filter(client=client, created__gte=before)
    for order in orders:
        products = order.products.all()
        for product in products:
            product_set.add(product.name)
    print(product_set)

    return render(request, 'all_products_from_orders.html',
                  {'client': client, 'products': product_set, 'days': days})


def product(request, pk: int):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})


def product_form(request):
    message = ''
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            count = form.cleaned_data['count']
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
            product = Product(
                name=name, description=description, price=price, count=count,
                image=image)
            product.save()
        message = 'Запись изменена'
    else:
        form = ProductForm()
        message = 'Заполните форму'
    return render(
        request, 'form.html', {
            'form': form, 'message': message,
        })