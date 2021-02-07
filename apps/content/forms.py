from captcha.fields import ReCaptchaField
from django import forms

from .models import CERT_TYPE_CHOICES, MultipleChoiceQuestion, Service
from .utils import ProfanityFilter, detect_profanity


class AddServiceForm(ProfanityFilter, forms.ModelForm):
    user_text_fields = ["service", "description"]

    class Meta:
        model = Service
        fields = ("service", "description")


class SubmitQuestionForm(ProfanityFilter, forms.ModelForm):
    cert_type = forms.ChoiceField(label="Certification", choices=CERT_TYPE_CHOICES)
    question = forms.CharField(
        label="Question",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 20}),
    )
    choice1 = forms.CharField(
        label="Choice #1",
        widget=forms.Textarea(attrs={"rows": 1, "cols": 20}),
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
    captcha = ReCaptchaField(label="")

    user_text_fields = [
        "question",
        "choice1",
        "choice2",
        "choice3",
        "choice4",
        "answers",
        "reference",
    ]

    class Meta:
        model = MultipleChoiceQuestion
        exclude = ("approved",)
