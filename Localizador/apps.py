from django.apps import AppConfig



class LocalizadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Localizador'
    
    def ready(self):
        import Localizador.signals