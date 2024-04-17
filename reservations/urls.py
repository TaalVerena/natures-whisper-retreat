from django.urls import path
from .views import make_reservation, calendar_events, reservation_confirmation,get_booked_dates

urlpatterns = [
    path("reserve/<int:lodge_id>/", make_reservation, name="make_reservation"),
    path("events/<int:lodge_id>/", calendar_events, name="calendar_events"),
    path('confirmation/<int:reservation_id>/', reservation_confirmation, name='reservation_confirmation'),
    path('booked-dates/<int:lodge_id>/', get_booked_dates, name='booked-dates'),
]
