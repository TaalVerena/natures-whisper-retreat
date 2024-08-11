from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    """
    Configuration class for the 'reservations' app.
    Sets default auto field type and app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "reservations"
