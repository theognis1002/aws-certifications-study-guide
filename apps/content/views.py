import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import AddServiceForm, SubmitQuestionForm
from .models import MultipleChoiceQuestion, Service
from .utils import clean_text


class HomeView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "home"
        return context


class PracticeQuizStartView(TemplateView):
    template_name = "content/practice_quiz_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "quiz-list"
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

        messages.success(self.request, "New AWS service added successfully!", extra_tags="success")
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
        if self.request.session.get("services"):
            queryset = self.request.session["services"]
        else:
            queryset = list(Service.objects.values().order_by("?"))
            self.request.session["services"] = queryset
        return queryset


class SubmitQuestionView(CreateView):
    model = MultipleChoiceQuestion
    template_name = "content/submit_question_form.html"
    form_class = SubmitQuestionForm
    success_url = reverse_lazy("submit-question")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "submit-question"
        return context

    def form_valid(self, form):
        cert_type = form.cleaned_data["cert_type"]
        choice1 = form.cleaned_data["choice1"]
        choice2 = form.cleaned_data["choice2"]
        choice3 = form.cleaned_data["choice3"]
        choice4 = form.cleaned_data["choice4"]
        answers = form.cleaned_data["answers"]
        question = form.cleaned_data["question"]

        messages.success(
            self.request,
            "Multiple choice question added successfully! It will be reviewed by an admin before appearing on the site.",
            extra_tags="success",
        )
        return super().form_valid(form)


class MultipleChoiceQuiz(ListView):
    context_object_name = "questions"
    template_name = "content/multiple_choice_quiz.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "multiple-choice-quiz"
        context["answer_key"] = self.request.session["answer_key"]
        return context

    def get_queryset(self):
        if self.request.session.get("questions"):
            queryset = self.request.session["questions"]
        else:
            queryset = list(MultipleChoiceQuestion.objects.filter(approved=True).values().order_by("?"))
            self.request.session["questions"] = queryset

        self.request.session["answer_key"] = [question["answers"] for question in queryset]
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
        score, num_correct, num_questions, incorrect_answers = self.get_score()
        context["score"] = score
        context["num_correct"] = num_correct
        context["num_questions"] = num_questions
        context["incorrect_answers"] = incorrect_answers

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
        questions = self.request.session["questions"]

        incorrect_answers = []
        num_correct = 0
        for idx, (correct_answer, user_answer, question) in enumerate(zip(answer_key, user_answers.values(), questions), 1):
            if correct_answer == user_answer:
                num_correct += 1
            else:
                question.update({"idx": idx, "user_answer": user_answer})
                incorrect_answers.append(question)

        num_questions = len(answer_key)
        score = (num_correct / num_questions) * 100
        return score, num_correct, num_questions, incorrect_answers


def retake_test_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    print("Session cleared!")
    return redirect(reverse_lazy("multiple-choice-quiz"))


class PracticeExamStartView(TemplateView):
    template_name = "content/practice_exams_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "practice-exam"
        return context


class PracticeExamView(ListView):
    context_object_name = "questions"
    template_name = "content/practice_exam.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "practice-exam"
        context["answer_key"] = self.request.session["answer_key"]
        if self.request.session.get("end_timer") is None:
            end_timer = (datetime.utcnow() + timedelta(minutes=65)).isoformat()
            self.request.session["end_timer"] = end_timer
        else:
            end_timer = self.request.session["end_timer"]
        context["end_timer"] = end_timer
        return context

    def get_queryset(self):
        if self.request.session.get("questions"):
            queryset = self.request.session["questions"]
        else:
            queryset = list(MultipleChoiceQuestion.objects.filter(approved=True).values().order_by("?")[:65])
            self.request.session["questions"] = queryset

        self.request.session["answer_key"] = [question["answers"] for question in queryset]
        return queryset


def end_timer(request):
    end_time = (datetime.utcnow() + timedelta(minutes=65)).isoformat()
    request.session["end_timer"] = end_time
    return JsonResponse({"time": end_time})


class FlashCardView(ListView):
    context_object_name = "services"
    template_name = "content/flash_card.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "flash-cards"
        return context

    def get_queryset(self):
        if self.request.session.get("flash_cards"):
            queryset = self.request.session["flash_cards"]
        else:
            queryset = list(Service.objects.values().order_by("?"))
            self.request.session["flash_cards"] = queryset

        return queryset


def flash_cards_redirect(request):
    del request.session["flash_cards"]
    return redirect(f"{reverse_lazy('flash-cards')}?page=2")


class ResourcesView(TemplateView):
    template_name = "content/resources.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "resources"


def test_route(request):
    request.session.clear()
    return JsonResponse({"message": "Session cleared!"})


# TODO add admin models - show not-approved questions, etc.
# TODO change dns to cloudflare
# TODO add ratelimiting
# TODO custom error pages
# TODO add social media
# TODO add stripe integration or donation page (?)
