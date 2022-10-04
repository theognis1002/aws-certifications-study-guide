from captcha.fields import ReCaptchaField
from django import forms

from .models import CERT_TYPE_CHOICES, MultipleChoiceQuestion, Service
from .utils import ProfanityFilter

ANSWER_CHOICES = [
    ("A", "Choice#1"),
    ("B", "Choice#2"),
    ("C", "Choice#3"),
    ("D", "Choice#4"),
]


class AddServiceForm(ProfanityFilter, forms.ModelForm):
    user_text_fields = ["service", "description"]

    class Meta:
        model = Service
        fields = ("service", "description")


class SubmitQuestionForm(ProfanityFilter, forms.ModelForm):
    cert_type = forms.ChoiceField(label="Certification Type", choices=CERT_TYPE_CHOICES)
    question = forms.CharField(
        label="Question",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 20}),
    )
    choice1 = forms.CharField(label="Choice #1")
    choice2 = forms.CharField(label="Choice #2")
    choice3 = forms.CharField(label="Choice #3")
    choice4 = forms.CharField(label="Choice #4")
    answers = forms.ChoiceField(label="Correct Answer", choices=ANSWER_CHOICES)
    reference = forms.CharField(
        label="Reference(s)",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 20,
                "placeholder": "Links to additional resources and/or reading materials",
            }
        ),
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
