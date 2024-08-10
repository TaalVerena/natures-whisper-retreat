from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """Form for handling contact requests."""

    class Meta:
        model = ContactRequest
        fields = ["name", "email", "category", "message", "status", "lodge_reply"]

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        user = kwargs.pop("user", None)
        super(ContactForm, self).__init__(*args, **kwargs)

        # Make the 'name' and 'email' fields not required
        self.fields["name"].required = False
        self.fields["email"].required = False

        # Disable the 'status' and 'lodge_reply' fields for non-staff users
        if user and not user.is_staff:
            self.fields["status"].disabled = True
            self.fields["lodge_reply"].disabled = True
