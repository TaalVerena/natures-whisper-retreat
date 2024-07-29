from django import forms
from .models import LodgeOverview
from django_summernote.widgets import SummernoteWidget


class LodgeOverviewForm(forms.ModelForm):
    """
    Form for creating and updating lodge overviews.
    """

    class Meta:
        model = LodgeOverview
        fields = ["name", "description", "image"]
        widgets = {
            "description": SummernoteWidget(),
        }
