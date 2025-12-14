# Localizador/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import views as auth_views
from . import api_views


urlpatterns = [
    # Reportes
    path('reportes/', login_required(views.listar_reportes), name='listar_reportes'),
    path('reportes/agregar/', views.agregar_reporte, name='agregar_reporte'),
    path('reportes/editar/<int:id>/', views.editar_reporte, name='editar_reporte'),
    path('reportes/eliminar/<int:id>/', views.eliminar_reporte, name='eliminar_reporte'),

    # Usuarios (solo admin, no login común)
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Zonas
    path('zonas/', views.listar_zonas, name='listar_zonas'),
    path('zonas/agregar/', views.agregar_zona, name='agregar_zona'),
    path('zonas/editar/<int:id>/', views.editar_zona, name='editar_zona'),
    path('zonas/eliminar/<int:id>/', views.eliminar_zona, name='eliminar_zona'),

    path('login/', auth_views.LoginView.as_view(template_name='Localizador/login.html'), name='login'),
    path('reportes/eliminar/<int:id>/', views.eliminar_reporte, name='eliminar_reporte'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Crear cuenta
    path('crear_cuenta/', views.crear_usuario, name='crear_cuenta'),

    path('api/estado/', api_views.api_estado, name='api_estado'),    
    path('api/zonas/', api_views.zonas_mapa, name='api_zonas'),
    path('mapa/', views.mapa_zonas, name='mapa_zonas'),
]
