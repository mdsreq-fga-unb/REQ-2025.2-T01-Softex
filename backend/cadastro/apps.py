from django.apps import AppConfig

class CadastroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastro'

    def ready(self):
        import cadastro.signals