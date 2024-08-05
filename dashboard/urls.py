from django.urls import path
from .views import (
    dashboard,
    reservation_list,
    edit_reservation,
    change_reservation_status,
)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/reservations/", reservation_list, name="reservation_list"),
    path("edit-reservation/<int:pk>/", edit_reservation, name="edit_reservation"),
    path("change-status/<int:pk>/", change_reservation_status, name="change_status"),
]
