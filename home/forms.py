from django import forms
from .models import LodgeOverview
from django_summernote.widgets import SummernoteWidget


class LodgeOverviewForm(forms.ModelForm):
    """
    Form for creating and updating lodge overviews.
    """

    def __init__(self, *args, **kwargs):
        super(LodgeOverviewForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'style': 'max-width: 570px;',
            'class': 'form-control'
        })

    class Meta:
        """
        Meta configuration for LodgeOverviewForm.
        """
        model = LodgeOverview
        fields = ["name", "description", "image"]
        widgets = {
            "description": SummernoteWidget(),
        }
