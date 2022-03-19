from django.conf import settings
from django.db import models
from mainapp.models import Product


class FavoriteProducts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
