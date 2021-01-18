from django import forms
from .models import Question


class AddQuestionForm(forms.ModelForm):
    answer_str = forms.CharField()

    class Meta:
        model = Question
        fields = ("question_type", "question", "answer_str")
