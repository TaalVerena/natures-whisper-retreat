from django import forms
from .models import Lodge
from django_summernote.widgets import SummernoteWidget


class LodgeForm(forms.ModelForm):
    """
    Form for creating and updating lodges.
    """

    class Meta:
        """
        Meta class to specify the model and fields.
        """

        model = Lodge
        fields = [
            "name",
            "description",
            "amenities",
            "image",
            "amenityImage1",
            "amenityImage2",
            "sleeps",
            "rate",
        ]
        widgets = {
            "description": SummernoteWidget(),
            "amenities": SummernoteWidget(),
        }
