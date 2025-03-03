from django import forms
from .models import Deal


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = "__all__"
        widgets = {
            "deal_date": forms.DateInput(attrs={"type": "date"}),
        }


class ReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    managers = forms.MultipleChoiceField(
        choices=Deal.MANAGER_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
