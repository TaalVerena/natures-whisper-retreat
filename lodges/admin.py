from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Lodge

@admin.register(Lodge)
class LodgeAdmin(SummernoteModelAdmin):
    list_display = ['name', 'rate'] 
    fieldsets = (
        (None, {
            'fields': ('name', 'rate')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('description', 'amenities'),
        }),
    )
    summernote_fields = ('description', 'amenities') 