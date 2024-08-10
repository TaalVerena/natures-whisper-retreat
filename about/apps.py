from django.apps import AppConfig


class AboutConfig(AppConfig):
    """
    Configuration class for 'about' app with default auto field.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
