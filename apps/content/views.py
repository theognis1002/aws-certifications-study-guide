from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import AddQuestionForm
from .models import Answer, Question


class QuizView(TemplateView):
    template_name = "content/quiz.html"


class AddQuestionView(FormView):
    template_name = "content/question_form.html"
    form_class = AddQuestionForm
    success_url = reverse_lazy("add-question")

    def form_valid(self, form):
        question_type = form.cleaned_data["question_type"]
        question = form.cleaned_data["question"]
        answer_str = form.cleaned_data["answer_str"]

        if question_type == "describe_service" or question_type == "choose_service":
            answer_type = "services"

        answer, created = Answer.objects.get_or_create(
            answer_type=answer_type, answer=answer_str
        )

        Question.objects.create(
            question_type=question_type, question=question, answer=answer
        )

        messages.success(
            self.request, "Question added successfully!", extra_tags="success"
        )
        return super().form_valid(form)
