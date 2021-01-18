from django.db import models


QUESTION_TYPE_CHOICES = [
    ("describe_service", "describe_service"),
    ("choose_service", "choose_service"),
    ("services", "services"),
    ("billing", "billing"),
    ("general", "general"),
]


class Answer(models.Model):
    answer_type = models.CharField(max_length=255, choices=QUESTION_TYPE_CHOICES)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer

    class Meta:
        ordering = ["answer"]


class Question(models.Model):
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPE_CHOICES)
    question = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.pk} - {self.question}"
