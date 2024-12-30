from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.views import View
from django.shortcuts import redirect
from core import views
import os
import json

class FrontendAppView(View):
    def get(self, request):
        try:
            if request.path.startswith('/admin/') or request.path.startswith('/test/'):
                return HttpResponseServerError("Invalid path")

            manifest_path = os.path.join(settings.REACT_BUILD_DIR, 'manifest.json')
            if not os.path.exists(manifest_path):
                raise FileNotFoundError(f"Manifest file not found at {manifest_path}")

            with open(manifest_path, 'r') as manifest_file:
                manifest = json.load(manifest_file)

            main_js = manifest.get('main.js', '/static/js/main.js')
            main_css = manifest.get('main.css', '/static/css/main.css')

            index_path = os.path.join(settings.REACT_BUILD_DIR, 'index.html')
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"Index file not found at {index_path}")

            with open(index_path, 'r') as index_file:
                html = index_file.read()
                html = html.replace('<!-- APP_JS -->', f'<script type="text/javascript" src="{main_js}"></script>')
                html = html.replace('<!-- APP_CSS -->', f'<link rel="stylesheet" href="{main_css}">')

            return HttpResponse(html)

        except Exception as e:
            return HttpResponseServerError(f"Error: {str(e)}")

def redirect_to_admin_login(request):
    return redirect('/admin/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('register/', views.register, name='register'),
    path('login/', redirect_to_admin_login),
    path('welcome/', views.welcome_view, name='welcome'),
    path('', FrontendAppView.as_view(), name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)