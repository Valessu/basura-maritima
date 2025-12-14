from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario
from datetime import date
from django.contrib.auth.hashers import make_password

@receiver(post_save, sender=User)
def crear_usuario_relacionado(sender, instance, created, **kwargs):
    if created:
        # Crear el Usuario personalizado asociado al User
        Usuario.objects.create(
            nombre_completo=instance.username,
            email=instance.email,
            password_hash=make_password(""),  # password no se usa
            rol="usuario",
            fecha_registro=date.today()
        )
