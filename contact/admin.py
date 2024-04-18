from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """Admin interface for managing contact requests."""
    
    list_display = ['name', 'email', 'category', 'created_at', 'closed']
    list_filter = ['category', 'closed']
    search_fields = ['name', 'email']
    actions = ['mark_as_closed']

    def mark_as_closed(self, request, queryset):
        """Action to mark selected requests as closed."""
        queryset.update(closed=True)
    mark_as_closed.short_description = "Mark selected requests as closed"
