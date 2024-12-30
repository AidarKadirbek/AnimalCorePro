from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.urls import reverse

def generate_activation_link(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse('activate_user', kwargs={'uidb64': uid, 'token': token})
    full_link = f"http://localhost:8000{activation_url}"
    return full_link

def send_activation_email(user, activation_link):
    email_subject = "Activate your account"
    email_body = f"""
    Здравствуйте, {user.username}!
    Пожалуйста, активируйте ваш аккаунт по ссылке: {activation_link}
    """
    send_mail(email_subject, email_body, 'animalcorepro@yandex.ru', [user.email])

def create_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://localhost:3000/activate/{uid}/{token}/"
    return activation_link