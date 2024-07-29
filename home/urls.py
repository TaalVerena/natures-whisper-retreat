from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("edit/<int:pk>/", views.edit_lodge_overview, name="edit_lodge_overview"),
]
