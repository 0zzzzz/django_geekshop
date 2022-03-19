from django.urls import path
from interkassaapp import views as inter

app_name = 'interkassaapp'

urlpatterns = [
    path('result/', inter.result, name='result'),
    path('success/', inter.success, name='success'),
    path('fail/', inter.fail, name='fail'),
    path('wait/', inter.wait, name='wait'),
    path('balance/', inter.balance, name='balance'),
]
