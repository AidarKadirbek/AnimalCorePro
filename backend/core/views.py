from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
import requests
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from .serializers import RegisterSerializer, UserSerializer
from .models import AnimalType, Breed, Animal, Weighting
from .serializers import AnimalTypeSerializer, BreedSerializer, AnimalSerializer, WeightingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .utils import send_activation_email
from .utils import generate_activation_link
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import AllowAny


User = get_user_model()

class AnimalTypeViewSet(viewsets.ModelViewSet):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    permission_classes = [IsAuthenticated]

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated]

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]

class WeightingViewSet(viewsets.ModelViewSet):
    queryset = Weighting.objects.all()
    serializer_class = WeightingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(id=self.request.user.id)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        if not request.user.is_staff:
            return Response({'detail': 'Недостаточно прав для выполнения операции.'}, status=status.HTTP_403_FORBIDDEN)
        user.toggle_active()
        return Response({'status': 'Активность пользователя изменена.', 'is_active': user.is_active})

@api_view(['GET'])
def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        return Response({"message": "Аккаунт успешно активирован!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Ссылка активации недействительна или истекла."}, status=status.HTTP_400_BAD_REQUEST)

def register(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm_password'),
        }
        response = requests.post('http://127.0.0.1:8000/core/api/register/', json=data)

        if response.status_code == 201:
            messages.success(request, "Ваш аккаунт был создан! Проверьте почту для активации.")
            return redirect('login')
        else:
            errors = response.json()
            return render(request, 'admin/register.html', {'errors': errors})

    return render(request, 'admin/register.html')

@api_view(['POST'])
def register_user(request):
    print(f"Request data: {request.data}")
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()

        activation_link = generate_activation_link(user)
        send_activation_email(user, activation_link)

        return Response({"message": "Пользователь успешно создан. Проверьте вашу почту для активации аккаунта."},
                        status=status.HTTP_201_CREATED)
    print(f"Serializer errors: {serializer.errors}")
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт успешно создан! Проверьте вашу почту для активации.")
            return redirect('login')
        else:
            print(f"Form errors: {form.errors}")
            return render(request, 'admin/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'admin/register.html', {'form': form})

def UserCreationView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт был создан!')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'admin/register.html', {'form': form})

@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        if user.is_staff:
            user_status = "staff"
        else:
            user_status = "user"

        return Response({
            "token": token.key,
            "status": user_status
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("admin:index")
    else:
        form = AuthenticationForm()

    return render(request, "admin/login.html", {"form": form, "title": "Войти в систему"})

class AnimalList(APIView):
    def get(self, request):
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)

def welcome_view(request):
    links = [
        {"name": "Список животных", "url": "/core/api/animals/"},
        {"name": "Режим администратора", "url": "/admin/"},
    ]
    return JsonResponse({
        "message": "Добро пожаловать на главную страницу!",
        "links": links
    })

class WeightingListView(ListView):
    model = Weighting
    template_name = 'core/weighting_list.html'
    context_object_name = 'weightings'

def edit_weighting(request, id):
    weighting = get_object_or_404(Weighting, id=id)
    return render(request, 'core/weighting_edit.html', {'weighting': weighting})

def delete_weighting(request, id):
    weighting = get_object_or_404(Weighting, id=id)
    if request.method == 'POST':
        weighting.delete()
        return redirect('weighting_list')
    return render(request, 'core/weighting_confirm_delete.html', {'weighting': weighting})

@api_view(['GET'])
def check_user_status(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Пользователь не аутентифицирован."}, status=status.HTTP_401_UNAUTHORIZED)

    is_staff = request.user.is_staff
    return Response({"is_staff": is_staff})