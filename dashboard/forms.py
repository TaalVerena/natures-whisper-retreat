from django import forms
from reservations.models import Reservation
from django.contrib.auth.models import User


class ReservationForm(forms.ModelForm):
    """
    Form for creating and updating reservations.
    """
    class Meta:
        """
        Meta configuration for ReservationForm.
        """
        model = Reservation
        fields = ["user", "lodge", "start_date", "end_date", "status"]


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        """
        Meta configuration for ProfileForm.
        """
        model = User
        fields = ["username", "email", "first_name", "last_name"]
