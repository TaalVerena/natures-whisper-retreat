from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'guests']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'start_date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'end_date'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control'})
        }