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
    list_display = ['name', 'rate', 'sleeps']
    fieldsets = (
        (None, {
            'fields': ('name',
                       'rate',
                       'sleeps',
                       'image',
                       'amenityImage1',
                       'amenityImage2'
                       )
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('description', 'amenities'),
        }),
    )
    summernote_fields = ('description', 'amenities')
