from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for managing contact requests.
    """

    # Fields to display in the admin list view
    list_display = ["name", "email", "category", "created_at", "closed"]

    # Filters for the list view
    list_filter = ["category", "closed"]

    # Fields searchable in the admin interface
    search_fields = ["name", "email"]

    # Custom actions available in the admin interface
    actions = ["mark_as_closed"]

    def mark_as_closed(self, request, queryset):
        """
        Mark selected contact requests as closed.
        """
        queryset.update(closed=True)

    mark_as_closed.short_description = "Mark selected requests as closed"
