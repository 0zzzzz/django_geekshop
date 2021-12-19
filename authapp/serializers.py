from django.contrib.auth import authenticate
from rest_framework import serializers
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = ShopUser
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return ShopUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class LoadSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=255)
    quantity = serializers.CharField(max_length=255)

    def postman(self, data):
        print(data)
        print(data)
        products = data
        for product in products:
            category_name = product['category']
            category_item = ProductCategory.objects.get(name=category_name)
            product['category'] = category_item
            Product.objects.create(**product)
            return {
                'email': product.category,
                'username': product.name,
                'token': product.price,
            }
