from django.urls import path
from . import views

urlpatterns = [
    path("", views.lodge_list, name="lodges"),
    path("<int:pk>/", views.lodge_detail, name="lodge_detail"),
    path("add/", views.add_lodge, name="add_lodge"),
    path("<int:pk>/edit/", views.edit_lodge, name="edit_lodge"),
    path("<int:pk>/delete/", views.delete_lodge, name="delete_lodge"),
]
