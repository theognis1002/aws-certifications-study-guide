from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("add-answer/", views.AddAnswerView.as_view(), name="add-answer"),
    path("add-question/", views.AddQuestionView.as_view(), name="add-question"),
    path("services-quiz/", views.ServicesQuiz.as_view(), name="services-quiz"),
    path("flash-cards/", views.FlashCardView.as_view(), name="flash-cards"),
    path("support/", views.SupportView.as_view(), name="support"),
]
