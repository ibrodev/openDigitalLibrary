from django.apps import AppConfig


class OdlauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'odlauth'
    verbose_name = 'odl custom authentication'
    
    def ready(self):
        
        from . import signals
