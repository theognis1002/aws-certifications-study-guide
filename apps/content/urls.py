from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("add-service/", views.AddServiceView.as_view(), name="add-service"),
    path("services-quiz/", views.ServicesQuiz.as_view(), name="services-quiz"),
    path("flash-cards/", views.FlashCardView.as_view(), name="flash-cards"),
    path("test/", views.test_route, name="test"),
]
