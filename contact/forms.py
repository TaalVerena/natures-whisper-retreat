from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """Form for handling contact requests."""
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'category', 'message']

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False
