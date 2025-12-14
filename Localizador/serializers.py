
from rest_framework import serializers
from .models import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['reporte_id', 'zona', 'usuario', 'creador', 'fecha_creacion']
