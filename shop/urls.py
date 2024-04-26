from django.urls import path
from .views import (client_products, delete_client, get_client,
                        get_clients, index, order, product, product_form)

urlpatterns = [
    path('', index, name='index'),
    path('clients/', get_clients, name='clients'),
    path('clients/<int:pk>/', get_client, name='get_client'),
    path('clients/<int:pk>/orders/', order, name='order'),
    path('clients/<int:pk>/orders/<int:days>/',
         client_products, name='client_products'),
    path('clients/delete/<int:pk>/', delete_client, name='delete'),
    path('product/<int:pk>', product, name='product'),
    path('product_form/', product_form, name='product_form'),
]