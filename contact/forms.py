from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """
    Form for contact requests; hides 'status' and 'lodge_reply'
    on creation and restricts 'lodge_reply' for non-staff users.
    """
    class Meta:
        model = ContactRequest
        fields = ["name", "email", "category", "message", "status", "lodge_reply"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, applying user-specific field settings.
        """
        user = kwargs.pop("user", None)
        super(ContactForm, self).__init__(*args, **kwargs)

        # Setting 'status' and 'lodge_reply' to hidden only on creation
        if not self.instance.pk:
            self.fields["status"].widget = forms.HiddenInput()
            self.fields["status"].initial = "pending"
            self.fields["lodge_reply"].widget = forms.HiddenInput()

        # Disable 'lodge_reply' for non-staff users when editing
        if user and not user.is_staff:
            self.fields["lodge_reply"].disabled = True
