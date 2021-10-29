from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from django.urls import reverse


@login_required
def basket(request):
    baskets_list = Basket.objects.filter(user=request.user)
    content = {
        'baskets': baskets_list
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()
    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)
    basket_item.quantity += 1
    basket_item.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
