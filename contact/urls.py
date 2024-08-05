from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
)

urlpatterns = [
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path(
        "contact/success/",
        TemplateView.as_view(template_name="contact/success.html"),
        name="contact_success",
    ),
    path("contact/edit/<int:pk>/", ContactUpdateView.as_view(), name="edit_contact_request"),
    path("contact/delete/<int:pk>/", ContactDeleteView.as_view(), name="delete_contact_request"),
]
