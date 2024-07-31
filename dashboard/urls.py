from django.urls import path
from .views import dashboard, reservation_list

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/reservations/", reservation_list, name="reservation_list"),
]
