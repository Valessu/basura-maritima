from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ZonaBasura


@api_view(['GET'])
def api_estado(request):
    return Response({
        "estado": "ok",
        "mensaje": "API funcionando correctamente"
    })


@api_view(['GET'])
def zonas_mapa(request):
    zonas = ZonaBasura.objects.filter(activo=True)

    data = []
    for z in zonas:
        data.append({
            "id": z.zona_id,
            "nombre": z.nombre,
            "descripcion": z.descripcion,
            "latitud": float(z.latitud),
            "longitud": float(z.longitud),
            "tipo_residuo": z.tipo_residuo,
            "nivel_contaminacion": z.nivel_contaminacion,
            "reportes": [
                {
                    "id": r.reporte_id,
                    "observaciones": r.observaciones,
                    "fecha": r.fecha_reporte
                }
                for r in z.reporte_set.all()
            ]
        })

    return Response(data)