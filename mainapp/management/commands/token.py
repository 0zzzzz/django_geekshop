from rest_framework.authtoken.models import Token
from django.core.management.base import BaseCommand
from authapp.models import ShopUser

class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            print(user)
            Token.objects.get_or_create(user=user)
            # print(Token.objects.get_or_create(user=user))
            print(Token.objects.get(user=user))
