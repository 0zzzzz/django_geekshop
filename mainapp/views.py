import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from django.views.generic import ListView
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from mainapp.context_processors import dollars
from favouritesapp.models import FavoriteProducts


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    # return random.sample(list(Product.objects.all()), 1)[0]
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related(
        'category')[:3]
    return products_list


def index(request):
    context = {
        'title': '??????????????',
        'products': get_products()[:4],
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': '????????????????',
    }
    return render(request, 'mainapp/contact.html', context)


@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()
    # links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': '??????',
                'pk': 0,
            }
        else:
            category_item = get_category(pk)
            products_list = get_products_in_category_orederd_by_price(pk)
        paginator = Paginator(products_list, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'links_menu': links_menu,
            'title': '????????????????',
            'category': category_item,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': '????????????????',
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    favorite = FavoriteProducts.objects.filter(product_id=pk, user_id=request.user)
    context = {
        'favorite': favorite,
        'product': get_product(pk),
        'price_in_dollars': float(get_product(pk).price) / dollars(request)['dollars'],
        'links_menu': get_links_menu(),
    }
    return render(request, 'mainapp/product.html', context)


def favorite_products(request):
    favorite = FavoriteProducts.objects.filter(user_id=request.user)
    context = {
        'favorite': favorite,
    }
    return render(request, 'mainapp/favorite_products.html', context)


class SearchResultsView(ListView):
    model = Product
    template_name = 'mainapp/search_results.html'


