# Localizador/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import ZonaBasura, Etiqueta, ZonaEtiqueta, Reporte, Imagen, Usuario
from .forms import ZonaBasuraForm, EtiquetaForm, ReporteForm, ImagenForm, UsuarioForm

def is_admin(user):
    return user.is_staff or user.is_superuser


# -------------------------
# Helpers
# -------------------------
def get_usuario_actual(request):
    """
    Devuelve el perfil Usuario asociado a request.user (auth.User).
    Para admins, devuelve None porque no se necesita perfil.
    """
    if request.user.is_staff or request.user.is_superuser:
        return None  # admin no necesita perfil
    try:
        return request.user.usuario
    except Usuario.DoesNotExist:
        return None

# -------------------------
# Registro público
# -------------------------
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse("Faltan datos.")

        # Crear User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        # Crear perfil Usuario
        Usuario.objects.create(
            user=user,
            nombre_completo=username,
            email=email,
            rol='user',
            password_hash=user.password,
            fecha_registro=date.today()
        )

        # Login automático
        user_auth = authenticate(request, username=username, password=password)
        if user_auth:
            auth_login(request, user_auth)
            return redirect('listar_reportes')

        return HttpResponse("Error al iniciar sesión.")

    return render(request, 'Localizador/crear_usuario.html')

# -------------------------
# Reportes
# -------------------------
@login_required
def listar_reportes(request):
    # Todos los usuarios ven todos los reportes
    reportes = Reporte.objects.all()
    return render(request, 'localizador/listar_reportes.html', {'reportes': reportes})

@login_required
def agregar_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            usuario_actual = get_usuario_actual(request)
            if usuario_actual:
                reporte.usuario = usuario_actual
            reporte.creador = request.user
            reporte.save()
            return redirect('listar_reportes')
    else:
        form = ReporteForm()
    return render(request, 'localizador/form_reporte.html', {'form': form, 'nombre_modelo': 'Reporte'})

@login_required
def editar_reporte(request, id):
    reporte = get_object_or_404(Reporte, pk=id)
    usuario_actual = get_usuario_actual(request)

    # Solo propietario o admin puede editar
    if not (request.user.is_staff or (usuario_actual and reporte.usuario == usuario_actual)):
        return HttpResponseForbidden("No tienes permiso para editar este reporte.")
    form = ReporteForm(request.POST or None, instance=reporte)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_reportes')

    return render(request, 'localizador/form_reporte.html', {'form': form, 'nombre_modelo': 'Reporte'})

@login_required
def eliminar_reporte(request, id):
    reporte = get_object_or_404(Reporte, pk=id)
    usuario_actual = get_usuario_actual(request)

    # Solo propietario o admin puede eliminar
    if not (request.user.is_staff or (usuario_actual and reporte.usuario == usuario_actual)):
        return HttpResponseForbidden("No tienes permiso para eliminar este reporte.")

    if request.method == 'POST':
        reporte.delete()
        return redirect('listar_reportes')

    return render(request, 'localizador/confirmar_eliminar.html', {
        'objeto_nombre': f"Reporte #{reporte.reporte_id}",
        'objeto_detalle': f"Zona: {reporte.zona} — Usuario: {reporte.usuario}",
        'volver_url': reverse('listar_reportes')
    })

# -------------------------
# Usuarios (admin)
# -------------------------
@login_required
@user_passes_test(is_admin)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "localizador/listar_usuarios.html", {
        "usuarios": usuarios
    })


@login_required
@user_passes_test(is_admin)
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Crear User
            django_user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password_hash']
            )
            # Crear perfil
            usuario = form.save(commit=False)
            usuario.user = django_user
            usuario.fecha_registro = timezone.now().date()
            usuario.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'localizador/form_usuario.html', {'form': form, 'nombre_modelo': 'Agregar Usuario'})

@login_required
@user_passes_test(is_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('listar_usuarios')
    return render(request, 'localizador/form_usuario.html', {'form': form, 'nombre_modelo': 'Editar Usuario'})

@login_required
@user_passes_test(is_admin)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'localizador/confirmar_eliminar.html', {
        'objeto_nombre': f"Usuario {usuario.nombre_completo}",
        'objeto_detalle': f"Email: {usuario.email}",
        'volver_url': reverse('listar_usuarios')
    })

# -------------------------
# Zonas, etiquetas e imágenes
# -------------------------
@login_required
def listar_zonas(request):
    return render(request, "localizador/listar_zonas.html", {"zonas": ZonaBasura.objects.all()})

@login_required
def agregar_zona(request):
    form = ZonaBasuraForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("listar_zonas")
    return render(request, "localizador/form_zona.html", {"form": form, "nombre_modelo": "Zona"})

@login_required
def editar_zona(request, id):
    zona = get_object_or_404(ZonaBasura, pk=id)
    form = ZonaBasuraForm(request.POST or None, instance=zona)
    if form.is_valid():
        form.save()
        return redirect('listar_zonas')
    return render(request, 'localizador/form_zona.html', {'form': form, 'nombre_modelo': 'Zona'})

@login_required
def eliminar_zona(request, id):
    zona = get_object_or_404(ZonaBasura, pk=id)
    if request.method == 'POST':
        zona.delete()
        return redirect('listar_zonas')
    return render(request, 'localizador/confirmar_eliminar.html', {
        'objeto_nombre': f"Zona {zona.nombre}",
        'objeto_detalle': zona.descripcion,
        'volver_url': reverse('listar_zonas')
    })

@login_required
def listar_etiquetas(request):
    return render(request, "localizador/listar_etiquetas.html", {"etiquetas": Etiqueta.objects.all()})

@login_required
def agregar_etiqueta(request):
    form = EtiquetaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("listar_etiquetas")
    return render(request, "localizador/form_etiqueta.html", {"form": form, "nombre_modelo": "Etiqueta"})

@login_required
def listar_imagenes(request):
    return render(request, "localizador/listar_imagenes.html", {"imagenes": Imagen.objects.all()})

@login_required
def agregar_imagen(request):
    form = ImagenForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("listar_imagenes")
    return render(request, "localizador/form_imagen.html", {"form": form, "nombre_modelo": "Imagen"})


@login_required
def mapa_zonas(request):
    return render(request, 'mapa_zonas.html')