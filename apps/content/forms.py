from django import forms
from .models import QUESTION_TYPE_CHOICES, Service, MultipleChoiceQuestion
from users.models import Support


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("service", "description")


class AddMultipleChoiceForm(forms.ModelForm):
    question = forms.CharField(
        label="Question", widget=forms.Textarea(attrs={"rows": 4, "cols": 20})
    )
    choice1 = forms.CharField(
        label="Choice #1", widget=forms.Textarea(attrs={"rows": 1, "cols": 20})
    )
    choice2 = forms.CharField(
        label="Choice #2",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
        required=False,
    )
    choice3 = forms.CharField(
        label="Choice #3",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
        required=False,
    )
    choice4 = forms.CharField(
        label="Choice #4",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
        required=False,
    )

    class Meta:
        model = MultipleChoiceQuestion
        fields = "__all__"


class SupportForm(forms.ModelForm):
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Support
        fields = "__all__"

    field_order = ["contact", "subject", "body"]
