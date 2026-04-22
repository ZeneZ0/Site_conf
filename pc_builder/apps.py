from django.apps import AppConfig

class PcBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pc_builder'

    def ready(self):
        import pc_builder.signals