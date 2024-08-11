from django import forms
from .models import Reservation
from datetime import date


class ReservationForm(forms.ModelForm):
    """
    Form for creating and updating reservations.
    """

    class Meta:
        model = Reservation
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "min": date.today().isoformat(),
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "min": date.today().isoformat(),
                }
            ),
        }
