from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from adminapp.forms import ShopUserAdminEdit, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, redirect
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = ShopUser.objects.all().order_by('-is_active')
        return context_data

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEdit(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserAdminEdit(instance=current_user)
    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        checkbox = request.POST.get('del_box', None)
        if checkbox:
            current_user.delete()
        else:
            if current_user.is_active:
                current_user.is_active = False
            else:
                current_user.is_active = True
            current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))
    context = {
        'user': get_object_or_404(ShopUser, pk=pk),
        'object': current_user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm()
    context = {
        'title': title,
        'form': category_form,
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {

        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=current_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm(instance=current_category)
    context = {
        'form': category_form,
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        checkbox = request.POST.get('del_box', None)
        if checkbox:
            current_category.delete()
        else:
            if current_category.is_active:
                current_category.is_active = False
            else:
                current_category.is_active = True
            current_category.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))
    context = {
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object': current_category,
    }
    return render(request, 'adminapp/category_delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#     title = 'продукт/создание'
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products_all'))
#     else:
#         product_form = ProductEditForm()
#     context = {
#         'title': title,
#         'form': product_form,
#     }
#     return render(request, 'adminapp/product_form.html', context)
class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    # success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        # return reverse('adminapp:product_list', args=[self.kwargs['pk']])
        # product_item = Product.objects.get(pk=self.kwargs['id'])
        return reverse('adminapp:products_all')

# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     context = {
#         'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active')
#     }
#     return render(request, 'adminapp/products.html', context)

class ProductsListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request, pk):
#     context = {
#
#         # 'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Product.objects.filter(pk=pk)
#     }
#     return render(request, 'adminapp/products.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     current_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         current_product = ProductEditForm(request.POST, request.FILES, instance=current_product)
#         if current_product.is_valid():
#             current_product.save()
#             return HttpResponseRedirect(reverse('adminapp:products_all'))
#     else:
#         current_product = ProductEditForm(instance=current_product)
#     context = {
#         'form': current_product,
#     }
#     return render(request, 'adminapp/product_form.html', context)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    # success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     current_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         checkbox = request.POST.get('del_box', None)
#         # print(request)
#         # print(request.method)
#         # print(current_product)
#         # print(checkbox)
#         if checkbox:
#             current_product.delete()
#         else:
#             if current_product.is_active:
#                 current_product.is_active = False
#             else:
#                 current_product.is_active = True
#             current_product.save()
#         # return HttpResponseRedirect(reverse('adminapp:product_list'))
#         return HttpResponseRedirect(reverse('adminapp:products_all'))
#         # return redirect(request.META.get('HTTP_REFERER'))
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#     context = {
#         # 'category': get_object_or_404(ProductCategory, pk=pk),
#         'product': get_object_or_404(Product, pk=pk),
#         'object': current_product,
#     }
#     return render(request, 'adminapp/product_delete.html', context)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))


@user_passes_test(lambda u: u.is_superuser)
def products_all(request):
    context = {
        # 'category': get_object_or_404(Product, pk=pk),
        'object_list': Product.objects.all(),
    }
    return render(request, 'adminapp/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
