from django import forms
from reservations.models import Reservation
from .models import Profile
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
    contact_number = forms.CharField(max_length=15, required=False, label="Contact Number")

    class Meta:
        """
        Meta configuration for ProfileForm.
        """
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Load initial data for contact number from Profile model
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['contact_number'].initial = self.instance.profile.contact_number

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        if commit:
            user.save()
            # Ensure the Profile object exists
            profile, created = Profile.objects.get_or_create(user=user)
            profile.contact_number = self.cleaned_data['contact_number']
            profile.save()
        return user