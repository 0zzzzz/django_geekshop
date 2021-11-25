from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from adminapp.forms import ShopUserAdminEdit, ProductCategoryEditForm, ProductEditForm, ProductCategoryCreateForm, \
    ProductCreateForm, ShopUserProfileEdit
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeleteClass:
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        if request.method == 'POST':
            checkbox = request.POST.get('del_box', None)
        if checkbox:
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            self.object = self.get_object()
            if self.object.is_active:
                self.object.is_active = False
            else:
                self.object.is_active = True
            self.object.save()
            return HttpResponseRedirect(success_url)


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


class UserDeleteView(AccessMixin, DeleteClass, DeleteView, ):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ProductCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:category_list')
    form_class = ProductCategoryCreateForm


class ProductCategoriesListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = ProductCategory.objects.all().order_by('-is_active')
        return context_data


class ProductCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:category_list')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


class ProductCategoryDeleteView(AccessMixin, DeleteClass, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'

    def get_success_url(self):
        return reverse('adminapp:category_list')


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

    def get(self, request, **kwargs):
        form = ProductCreateForm(initial={'category': get_object_or_404(ProductCategory, pk=self.kwargs['pk'])})
        return render(request, 'adminapp/product_form.html', {'form': form})


class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDeleteView(AccessMixin, DeleteClass, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'


class OrdersListView(AccessMixin, ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Order.objects.filter(user_id=self.kwargs.get('pk')).order_by('-is_active')
        return context_data

    def get_queryset(self):
        return Order.objects.filter(user_id=self.kwargs.get('pk'))

    # class OrdersCreateView(AccessMixin, CreateView):
    #     model = Order
    #     template_name = 'adminapp/product_form.html'
    #     form_class = ProductCreateForm
    #
    #     def get_success_url(self):
    #         product_item = Product.objects.get(pk=self.kwargs['pk'])
    #         return reverse('adminapp:product_list', args=[product_item.category_id])
    #
    #     def get(self, request, **kwargs):
    #         form = ProductCreateForm(initial={'category': get_object_or_404(ProductCategory, pk=self.kwargs['pk'])})
    #         print(form['category'])
    #         return render(request, 'adminapp/product_form.html', {'form': form})

    # class OrdersUpdateView(AccessMixin, UpdateView):
    # model = Order
    # template_name = 'adminapp/order_edit.html'
    # form_class = ProductEditForm
    #
    # def get_success_url(self):
    #     product_item = Product.objects.get(pk=self.kwargs['pk'])
    #     return reverse('adminapp:product_list', args=[product_item.category_id])


class OrderUpdateView(AccessMixin, UpdateView):
    model = Order
    fields = []
    template_name = 'adminapp/order_edit.html'
    # success_url = reverse_lazy('adminapp:orders_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)

    def get_success_url(self):
        order_item = Order.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:orders_list', args=[order_item.user_id])


class OrderDeleteView(AccessMixin, DeleteClass, DeleteView):
    model = Order
    template_name = 'adminapp/order_delete.html'

    def get_success_url(self):
        order_item = Order.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:orders_list', args=[order_item.user_id])

    # def get_success_url(self):
    #     product_item = Product.objects.get(pk=self.kwargs['pk'])
    #     return reverse('adminapp:product_list', args=[product_item.category_id])


class OrderDetailView(AccessMixin, DetailView):
    model = Order
    template_name = 'adminapp/order_detail.html'
