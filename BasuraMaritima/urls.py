# BasuraMaritima/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirección si se entra a la raíz
    path('', home_redirect, name='home'),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='Localizador/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # URLs de la app
    path('', include('Localizador.urls')),
]
