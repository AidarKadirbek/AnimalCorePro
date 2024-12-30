from .models import AnimalType, Breed, Animal, Weighting
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalType
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class WeightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weighting
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # Проверка совпадения паролей
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None)
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['is_staff']