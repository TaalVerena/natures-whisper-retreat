from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Configuration class for the 'contact' app.
    Sets default auto field type and app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "contact"
