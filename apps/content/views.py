from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView, ListView

from .forms import AddQuestionForm
from .models import Answer, Question
from .utils import clean_text


class HomeView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "home"
        return context


class QuizView(TemplateView):
    template_name = "content/quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "home"
        return context


class AddAnswerView(CreateView):
    model = Answer
    fields = "__all__"
    success_url = reverse_lazy("add-answer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "add-answer"
        return context

    def get_initial(self):
        initial = {"answer_type": "services"}
        return initial

    def form_valid(self, form):
        messages.success(
            self.request, "Answer added successfully!", extra_tags="success"
        )
        return super().form_valid(form)


class AddQuestionView(FormView):
    template_name = "content/question_form.html"
    form_class = AddQuestionForm
    success_url = reverse_lazy("add-question")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "add-question"
        return context

    def form_valid(self, form):
        question_type = form.cleaned_data["question_type"]
        question = form.cleaned_data["question"]
        answer = form.cleaned_data["answer"]
        answer_str = form.cleaned_data["answer_str"]

        question = clean_text(question)

        if question_type == "describe_service" or question_type == "choose_service":
            answer_type = "services"
        else:
            answer_type = question_type

        if len(answer_str) > 0:
            answer = answer_str

        answer_obj = Answer.objects.filter(answer__icontains=answer)
        if answer_obj.exists():
            answer_obj = answer_obj.first()
        else:
            answer_obj = Answer.objects.create(answer_type=question_type, answer=answer)

        Question.objects.create(
            question_type=question_type, question=question, answer=answer_obj
        )

        messages.success(
            self.request, "Question added successfully!", extra_tags="success"
        )
        return super().form_valid(form)


class ServicesQuiz(ListView):
    context_object_name = "services"
    template_name = "content/services_quiz.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "services-quiz"
        return context

    def get_queryset(self):
        return Question.objects.filter(question_type="services")


class FlashCardView(ListView):
    context_object_name = "services"
    template_name = "content/flash_card.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "flash-cards"
        return context

    def get_queryset(self):
        return Question.objects.filter(question_type="services").order_by("?")
