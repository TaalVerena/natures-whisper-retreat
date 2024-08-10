from django.urls import path
from contact.views import ContactUpdateView, ContactDeleteView

from .views import (
    dashboard,
    reservation_list,
    edit_reservation,
    change_reservation_status,
    delete_reservation,
    view_reservation,
    profile_view,
)


# URL patterns for dashboard and reservation-related views
urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/reservations/", reservation_list, name="reservation_list"),
    path("edit-reservation/<int:pk>/", edit_reservation, name="edit_reservation"),
    path("change-status/<int:pk>/", change_reservation_status, name="change_status"),
    path(
        "delete-reservation/<int:pk>/",
        delete_reservation,
        name="delete_reservation",
    ),
    path("view-reservation/<int:pk>/", view_reservation, name="view_reservation"),
    path(
        "contact/edit/<int:pk>/",
        ContactUpdateView.as_view(),
        name="edit_contact_request",
    ),
    path(
        "contact/delete/<int:pk>/",
        ContactDeleteView.as_view(),
        name="delete_contact_request",
    ),
    path("profile/", profile_view, name="profile"),
]
