from django.urls import path
from . import views

# URL patterns for the home app
urlpatterns = [
    path("", views.home_view, name="home"),
    path("edit/<int:pk>/", views.edit_lodge_overview, name="edit_lodge_overview"),
]
