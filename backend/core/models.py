from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.db import models

class AnimalType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Тип животного"))

    def __str__(self):
        return self.name

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Порода"))
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, verbose_name=_("Тип животного"))

    def __str__(self):
        return f"{self.name} ({self.animal_type})"

class Animal(models.Model):
    inventory_number = models.CharField(max_length=100, unique=True, verbose_name=_("Инвентарный номер"))
    gender = models.CharField(max_length=10, verbose_name=_("Пол"))
    name = models.CharField(max_length=100, verbose_name=_("Имя"))
    arrival_date = models.DateField(verbose_name=_("Дата поступления"))
    age_at_arrival = models.IntegerField(verbose_name=_("Возраст на момент поступления (в месяцах)"))
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name=_("Порода"))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Родитель"))

    def __str__(self):
        return self.name

class Weighting(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name=_("Животное"))
    date = models.DateField(verbose_name=_("Дата взвешивания"))
    weight = models.FloatField(default=0.0, verbose_name=_("Вес"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))

    class Meta:
        permissions = [
            ("can_view_own_weightings", "Can view own weightings"),
            ("can_change_own_weightings", "Can change own weightings"),
        ]
        unique_together = ('animal', 'date')

    def __str__(self):
        return f"{self.animal.name} - {self.date} - {self.weight}kg"

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен для пользователя')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

    def generate_activation_token(user):
        return default_token_generator.make_token(user)

    def get_activation_url(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = self.activation_token()
        return f'http://localhost:8000/core/api/activate/{uidb64}/{token}/'

    def toggle_active(self):
        self.is_active = not self.is_active
        self.save()