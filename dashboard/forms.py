from django import forms
from reservations.models import Reservation
from django.contrib.auth.models import User


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["user", "lodge", "start_date", "end_date", "status"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
