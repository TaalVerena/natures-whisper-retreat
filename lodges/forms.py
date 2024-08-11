from django import forms
from .models import Lodge
from django_summernote.widgets import SummernoteWidget


class LodgeForm(forms.ModelForm):
    """
    Form for creating and updating lodges.
    """
    def __init__(self, *args, **kwargs):
        super(LodgeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'style': 'max-width: 570px;',
            'class': 'form-control'
        })

    class Meta:
        """
        Meta class to specify the model and fields.
        Configures the fields to include in the form and the widgets used.
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
