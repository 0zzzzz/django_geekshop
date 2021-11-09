from adminapp import views as admin_views
from django.urls import path

app_name = 'admin_views'

urlpatterns = [
    path('users/create/', admin_views.user_create, name='user_create'),
    path('users/', admin_views.users, name='user_list'),
    path('users/update/<int:pk>/', admin_views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', admin_views.user_delete, name='user_delete'),

    path('categories/create/', admin_views.category_create, name='category_create'),
    path('categories/', admin_views.categories, name='category_list'),
    path('categories/update/<int:pk>/', admin_views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', admin_views.category_delete, name='category_delete'),

    path('products/create/', admin_views.product_create, name='product_create'),
    path('products/', admin_views.products_all, name='products_all'),
    path('products/<int:pk>/', admin_views.products, name='product_list'),
    path('products/detail/<int:pk>/', admin_views.ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<int:pk>/', admin_views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', admin_views.product_delete, name='product_delete'),
]
