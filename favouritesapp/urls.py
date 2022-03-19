from django.urls import path
from favouritesapp import views as favourite

app_name = 'favouritesapp'

urlpatterns = [
    path('add/<int:pk>/', favourite.add, name='add'),
    path('remove/<int:pk>/', favourite.remove, name='remove'),
]
