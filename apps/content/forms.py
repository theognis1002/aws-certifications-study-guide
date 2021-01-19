from django import forms
from .models import QUESTION_TYPE_CHOICES, Service
from users.models import Support


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("service", "description")


class SupportForm(forms.ModelForm):
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Support
        fields = "__all__"

    field_order = ["contact", "subject", "body"]
