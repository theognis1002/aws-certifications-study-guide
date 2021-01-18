from django.urls import path
from . import views

urlpatterns = [
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("add-question/", views.AddQuestionView.as_view(), name="add-question"),
]
