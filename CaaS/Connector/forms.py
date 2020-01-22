from django import forms
from Connector.models import SSCConnector


class SSForm(forms.ModelForm):
    interval = forms.IntegerField()
    api_url = forms.URLField(max_length=255)
    api_token = forms.CharField()
    overall_score = forms.IntegerField()
    factor_score = forms.IntegerField()
    issue_level_event = forms.IntegerField()
    domain = forms.URLField()

    class Meta:
        model = SSCConnector
        fields = ('interval','api_url','api_token','overall_score','factor_score','issue_level_event','domain',)