from django.db import models
from django.contrib.auth.models import User



# ============================
# MODELOS QUE ADMINISTRARÁ DJANGO
# ============================


class Etiqueta(models.Model):
    etiqueta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'etiqueta'

    def __str__(self):
        return self.nombre


class Licencia(models.Model):
    licencia_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    url_legal = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'licencia'

    def __str__(self):
        return self.nombre


class ZonaBasura(models.Model):
    zona_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    tipo_residuo = models.CharField(max_length=50)
    nivel_contaminacion = models.CharField(max_length=7, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    licencia = models.ForeignKey(Licencia, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'zona_basura'

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ← ESTA ES LA CLAVE

    nombre_completo = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)
    fecha_registro = models.DateField()

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return self.nombre_completo

class Reporte(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    zona = models.ForeignKey(ZonaBasura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    cantidad_residuos_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_reporte = models.DateTimeField(blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reporte'

    def __str__(self):
        return f"Reporte {self.reporte_id}"


class Imagen(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    zona = models.ForeignKey(ZonaBasura, on_delete=models.SET_NULL, blank=True, null=True)
    reporte = models.ForeignKey(Reporte, on_delete=models.SET_NULL, blank=True, null=True)
    url_imagen = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'imagen'

    def __str__(self):
        return f"Imagen {self.imagen_id}"


class ZonaEtiqueta(models.Model):
    id = models.AutoField(primary_key=True)
    zona = models.ForeignKey(ZonaBasura, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'zona_etiqueta'
        unique_together = ('zona', 'etiqueta')

    def __str__(self):
        return f"{self.zona} - {self.etiqueta}"
