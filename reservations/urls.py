from django.urls import path
from .views import make_reservation

urlpatterns = [
    path('reserve/<int:lodge_id>/', make_reservation, name='make_reservation'),
]
