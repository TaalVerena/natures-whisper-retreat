from django.urls import path
from . import views

# URL patterns for about-related views
urlpatterns = [
    path("about/", views.about_view, name="about"),
]
