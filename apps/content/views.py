import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import AddServiceForm
from .models import Service
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


class FlashCardView(ListView):
    context_object_name = "services"
    template_name = "content/flash_card.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "flash-cards"
        return context

    def get_queryset(self):
        return Service.objects.all().order_by("?")


def test_route(request):
    with open("data.json") as f:
        data = json.load(f)

    # for row in data:
    #     Service.objects.create(
    #         service=row["answer__answer"], description=row["question"]
    #     )
    return JsonResponse(data, safe=False)
