from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    """
    Customizes the appearance and behavior of the Reservation model in the Django admin interface.
    """

    # Fields to display in the list view
    list_display = (
        "status",
        "lodge",
        "user",
        "start_date",
        "end_date",
        "duration_days",
    )

    # Filters for narrowing down the list of reservations
    list_filter = ("lodge", "start_date", "end_date", "user")

    # Searchable fields to help find specific reservations
    search_fields = ("lodge__name", "user__username", "user__email")

    # Enables date hierarchy navigation based on the start date
    date_hierarchy = "start_date"

    def duration_days(self, obj):
        """
        Computes and displays the duration of the reservation in days.

        Parameters:
            obj (Reservation): The reservation object.

        Returns:
            int: The number of days between start_date and end_date.
        """
        return (obj.end_date - obj.start_date).days

    # Sets a custom label for the duration_days method
    duration_days.short_description = "Duration (days)"


# Registers the Reservation model with the custom admin settings
admin.site.register(Reservation, ReservationAdmin)
