from django import forms
from django.core.exceptions import ValidationError
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")

            # Check for existing reservations overlapping with the selected dates
            existing_reservations = Reservation.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date,
            )

            if existing_reservations.exists():
                raise ValidationError("The selected dates overlap with an existing reservation.")

        return cleaned_data
