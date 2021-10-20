from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='products'),
    # path('<str:name>/', mainapp.products, name='category'),
    path('<int:pk>/', mainapp.products, name='category'),
]
