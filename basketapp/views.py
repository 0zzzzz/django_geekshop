from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def add(request, pk):
    # не знаю насколько это в дальнейшем понадобится, но так сайт не ломается при незалогиненом пользователе
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        basket = Basket.objects.filter(user=request.user, product=product).first()
        if not basket:
            basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
