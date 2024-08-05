from django import forms
from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["user", "lodge", "start_date", "end_date", "status"]


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["status"]
