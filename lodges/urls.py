from django.urls import path
from . import views

urlpatterns = [
    path('', views.lodge_list, name='lodges'),
]