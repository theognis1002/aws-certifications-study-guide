from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("add-service/", views.AddServiceView.as_view(), name="add-service"),
    path("services-quiz/", views.ServicesQuiz.as_view(), name="services-quiz"),
    path(
        "add-multiple-choice/",
        views.AddMultipleChoiceView.as_view(),
        name="add-multiple-choice",
    ),
    path(
        "multiple-choice-quiz/",
        views.MultipleChoiceQuiz.as_view(),
        name="multiple-choice-quiz",
    ),
    path(
        "mc-quiz-results/",
        views.MultipleChoiceQuizResults.as_view(),
        name="multiple-choice-quiz-results",
    ),
    path("flash-cards/", views.FlashCardView.as_view(), name="flash-cards"),
    path("test/", views.test_route, name="test"),
    path(
        "cloud-practitioner-quiz/answers/",
        views.add_answers_to_session,
        name="answers",
    ),
    path(
        "cloud-practitioner-quiz/user-answers/",
        views.get_previous_user_answers,
        name="user-answers",
    ),
]
