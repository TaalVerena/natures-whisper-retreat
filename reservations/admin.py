from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('lodge', 'user', 'start_date', 'end_date', 'guests', 'duration_days')
    list_filter = ('lodge', 'start_date', 'end_date', 'user')
    search_fields = ('lodge__name', 'user__username', 'user__email')
    date_hierarchy = 'start_date'

    def duration_days(self, obj):
        return (obj.end_date - obj.start_date).days
    duration_days.short_description = 'Duration (days)'

admin.site.register(Reservation, ReservationAdmin)