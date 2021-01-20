import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, RedirectView

from .forms import AddMultipleChoiceForm, AddServiceForm
from .models import MultipleChoiceQuestion, Service
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


class AddServiceView(CreateView):
    model = Service
    template_name = "content/service_form.html"
    form_class = AddServiceForm
    success_url = reverse_lazy("add-service")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "add-service"
        return context

    def form_valid(self, form):
        service = form.cleaned_data["service"]
        description = form.cleaned_data["description"]

        description = clean_text(description)

        messages.success(
            self.request, "New AWS service added successfully!", extra_tags="success"
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
        return Service.objects.all()


class AddMultipleChoiceView(CreateView):
    model = MultipleChoiceQuestion
    template_name = "content/multiple_choice_form.html"
    form_class = AddMultipleChoiceForm
    success_url = reverse_lazy("add-multiple-choice")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "add-multiple-choice"
        return context

    def form_valid(self, form):
        choice1 = form.cleaned_data["choice1"]
        choice2 = form.cleaned_data["choice2"]
        choice3 = form.cleaned_data["choice3"]
        choice4 = form.cleaned_data["choice4"]
        answers = form.cleaned_data["answers"]
        question = form.cleaned_data["question"]

        messages.success(
            self.request,
            "Multiple choice question added successfully!",
            extra_tags="success",
        )
        return super().form_valid(form)


class MultipleChoiceQuiz(ListView):
    context_object_name = "questions"
    template_name = "content/multiple_choice_quiz.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "multiple-choice-quiz"
        context["answer_key"] = self.request.session["answer_key"]
        return context

    def get_queryset(self):
        if self.request.session.get("questions"):
            queryset = self.request.session["questions"]
        else:
            queryset = list(MultipleChoiceQuestion.objects.values().order_by("?"))
            self.request.session["questions"] = queryset

        self.request.session["answer_key"] = [
            question["answers"] for question in queryset
        ]
        return queryset


def add_answers_to_session(request):
    json_response = json.loads(request.body)
    answers = json_response["answers"]

    if request.session.get("answers") is None:
        request.session["answers"] = answers
        user_answers = answers
    else:
        user_answers = request.session["answers"]
        user_answers.update(answers)
        request.session["answers"] = user_answers

    return JsonResponse(user_answers)


def get_previous_user_answers(request):
    if request.session.get("answers") is None:
        user_answers = {}
        request.session["answers"] = user_answers
    else:
        user_answers = request.session["answers"]

    return JsonResponse(user_answers)


class MultipleChoiceQuizResults(TemplateView):
    template_name = "content/quiz_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "multiple-choice-quiz"
        score, num_correct, num_questions = self.get_score()
        context["score"] = score
        context["num_correct"] = num_correct
        context["num_questions"] = num_questions

        if score > 85:
            score_color = "success"
        elif score > 70:
            score_color = "warning"
        else:
            score_color = "danger"

        context["score_color"] = score_color
        return context

    def get_score(self):
        answer_key = self.request.session["answer_key"]
        user_answers = self.request.session["answers"]

        num_correct = 0
        for correct_answer, user_answer in zip(answer_key, user_answers.values()):
            if correct_answer == user_answer:
                num_correct += 1

        num_questions = len(answer_key)
        score = (num_correct / num_questions) * 100
        return score, num_correct, num_questions


def retake_test_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    print("Session cleared!")
    return redirect(reverse_lazy("multiple-choice-quiz"))


class FlashCardView(ListView):
    context_object_name = "services"
    template_name = "content/flash_card.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "flash-cards"
        return context

    def get_queryset(self):
        return Service.objects.all()


def test_route(request):
    data = request.session["answers"]
    # with open("data.json") as f:
    #     data = json.load(f)

    return JsonResponse(data, safe=False)
