from django.urls import path
from .views import (
    make_reservation,
    reservation_confirmation,
    get_booked_dates,
)

# URL patterns for the reservations app
urlpatterns = [
    path("reserve/<int:lodge_id>/", make_reservation, name="make_reservation"),
    path("confirmation/<int:reservation_id>/", reservation_confirmation, name="reservation_confirmation"),
    path("booked-dates/<int:lodge_id>/", get_booked_dates, name="booked_dates"),
]
