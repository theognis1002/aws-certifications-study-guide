import pytest

from apps.users.models import MultipleChoiceQuestion, Service

pytestmark = pytest.mark.django_db


def test_service_str():
    service = Service.objects.create(
        name="Lambda", description="Serverless cloud function"
    )
    assert str(service) == "Lambda"


def test_multiple_choice_question_str():
    multiple_choice_question = MultipleChoiceQuestion.objects.create(
        question="What is the meaning of life?", answers="404 Not Found"
    )
    assert str(multiple_choice_question) == "What is the meaning of life?"
