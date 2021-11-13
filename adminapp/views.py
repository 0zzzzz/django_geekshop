from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from adminapp.forms import ShopUserAdminEdit, ProductCategoryEditForm, ProductEditForm, ProductCategoryCreateForm, \
    ProductCreateForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, redirect
from mainapp.models import Product, ProductCategory


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(AccessMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:user_list')
    form_class = ShopUserRegisterForm


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = ShopUser.objects.all().order_by('-is_active')
        return context_data


class UserUpdateView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEdit
    success_url = reverse_lazy('adminapp:user_list')


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


class ProductCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:category_list')
    form_class = ProductCategoryCreateForm


class ProductCategoriesListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'


class ProductCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:category_list')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


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


class ProductsListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductCreateForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # def get(self, *args, **kwargs):
    #     print('Processing GET request')
    #     resp = super().get(*args, **kwargs)
    #     print(resp)
    #     print('Finished processing GET request')
    #     return resp

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     print(self.form_class)
    #     self.form_class(
    #         initial={'category': get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))})
    #     return context_data
    # def get_queryset(self):
    #     print(Product.objects.filter(category__pk=self.kwargs.get('pk')))
    #     return Product.objects.filter(category__pk=self.kwargs.get('pk'))


# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductCreateForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductCreateForm(initial={'category': category})
#
#     content = {'title': title,
#                'form': product_form,
#                'category': category
#                }
#
#     return render(request, 'adminapp/product_form.html', content)


def get_success_url(self):
    product_item = Product.objects.get(pk=self.kwargs['pk'])
    return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDeleteView(AccessMixin, DeleteView):
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


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
