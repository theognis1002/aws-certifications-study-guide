from django import forms
from .models import Question, Answer, QUESTION_TYPE_CHOICES
from users.models import Support


class AddQuestionForm(forms.ModelForm):
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES, initial=QUESTION_TYPE_CHOICES[2][0]
    )
    answer = forms.ModelChoiceField(Answer.objects.all(), required=False)
    answer_str = forms.CharField(label="Answer String", required=False)

    class Meta:
        model = Question
        fields = ("question_type", "question", "answer", "answer_str")


class SupportForm(forms.ModelForm):
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = Support
        fields = "__all__"

    field_order = ["contact", "subject", "body"]
