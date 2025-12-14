from django.contrib import admin
from .models import Reporte, Usuario, ZonaBasura

# -------------------------
# USUARIO
# -------------------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'nombre_completo', 'email', 'rol', 'fecha_registro')
    search_fields = ('nombre_completo', 'email')


# -------------------------
# REPORTE
# -------------------------
@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte_id', 'zona', 'usuario', 'cantidad_residuos_kg', 'fecha_reporte', 'creador')
    list_filter = ('fecha_reporte', 'creador')
    search_fields = ('reporte_id', 'usuario__nombre_completo')
    readonly_fields = ('creador',)  # ← para que no se pueda editar manualmente

    def save_model(self, request, obj, form, change):
        # Si el registro es nuevo, asigna el creador automáticamente
        if not change:
            obj.creador = request.user
        super().save_model(request, obj, form, change)


# -------------------------
# ZONA BASURA
# -------------------------
@admin.register(ZonaBasura)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('zona_id', 'nombre', 'tipo_residuo', 'nivel_contaminacion', 'activo')
    list_filter = ('tipo_residuo', 'activo')
    search_fields = ('nombre',)

