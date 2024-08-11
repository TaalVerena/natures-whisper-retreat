from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Lodge


# Registers the Lodge model with the custom admin settings
@admin.register(Lodge)
class LodgeAdmin(SummernoteModelAdmin):
    """
    Customizes the appearance and behavior of
    the Lodge model in the Django admin interface.
    """
    # Fields to display in the admin list view
    list_display = ["name", "rate", "sleeps"]

    # Field layout in the admin form
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "rate",
                    "sleeps",
                    "image",
                    "amenityImage1",
                    "amenityImage2",
                )
            },
        ),
        (
            "Details",
            {
                "classes": ("collapse",),
                "fields": ("description", "amenities"),
            },
        ),
    )

    # Fields using the Summernote editor
    summernote_fields = ("description", "amenities")
