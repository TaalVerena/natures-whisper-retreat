from django.urls import path
from . import views

urlpatterns = [
    path('', views.lodge_list, name='lodges'),
    path('<int:pk>/', views.lodge_detail, name='lodge_detail'),
]