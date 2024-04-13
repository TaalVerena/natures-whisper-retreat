from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Lodge

# Register your models here.
@admin.register(Lodge)
class LodgeAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'amenities')