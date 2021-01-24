from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("quiz/", views.PracticeQuizStartView.as_view(), name="quiz-list"),
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
        "multiple-choice-quiz-results/",
        views.MultipleChoiceQuizResults.as_view(),
        name="multiple-choice-quiz-results",
    ),
    path(
        "redirect/",
        views.retake_test_view,
        name="retake-test",
    ),
    path("flash-cards/", views.FlashCardView.as_view(), name="flash-cards"),
    path(
        "flash-cards-redirect/",
        views.flash_cards_redirect,
        name="flash-cards-redirect",
    ),
    path(
        "practice-exam/start",
        views.PracticeExamStartView.as_view(),
        name="practice-exam-start",
    ),
    path(
        "end-timer/",
        views.end_timer,
        name="end-timer",
    ),
    path(
        "practice-exam/",
        views.PracticeExamView.as_view(),
        name="practice-exam",
    ),
    path("resources/", views.ResourcesView.as_view(), name="resources"),
    path("clear/", views.test_route, name="clear"),
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
