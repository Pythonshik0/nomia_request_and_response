from django import forms
from .models import Choice


class ResponseForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.all(), empty_label=None, widget=forms.RadioSelect)