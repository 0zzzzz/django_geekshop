from django.contrib import admin
from django.urls import path, include

from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('read/<pk>/', ordersapp.OrderListView.as_view(), name='read'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('update/<pk>/', ordersapp.OrderListView.as_view(), name='update'),
    path('delete/<pk>/', ordersapp.OrderListView.as_view(), name='delete'),
]