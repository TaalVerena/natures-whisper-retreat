from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    """
    Customizes the appearance and behavior of the Reservation model in the Django admin interface.
    """

    list_display = (
        "status",
        "lodge",
        "user",
        "start_date",
        "end_date",
        "duration_days",
    )
    list_filter = ("lodge", "start_date", "end_date", "user")
    search_fields = ("lodge__name", "user__username", "user__email")
    date_hierarchy = "start_date"

    def duration_days(self, obj):
        """
        Computes and displays the duration of the reservation in days.
        """
        return (obj.end_date - obj.start_date).days

    duration_days.short_description = "Duration (days)"


# Registers the Reservation model with the custom admin settings
admin.site.register(Reservation, ReservationAdmin)
