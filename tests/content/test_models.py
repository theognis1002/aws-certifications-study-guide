import pytest
from django.apps import apps

Service = apps.get_model("content", "Service")
MultipleChoiceQuestion = apps.get_model("content", "MultipleChoiceQuestion")

pytestmark = pytest.mark.django_db


def test_service_str():
    service = Service.objects.create(service="Lambda", description="Serverless cloud function")
    assert str(service) == "Lambda"


def test_multiple_choice_question_str():
    multiple_choice_question = MultipleChoiceQuestion.objects.create(question="What is the meaning of life?", answers="404 Not Found")
    assert str(multiple_choice_question) == "What is the meaning of life?"
