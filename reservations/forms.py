from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    """
    Form for creating a reservation.
    """
    class Meta:
        """
        Meta class defining the form behavior.
        """
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
