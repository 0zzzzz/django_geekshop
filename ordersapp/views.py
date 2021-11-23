from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ordersapp.models import Order


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

