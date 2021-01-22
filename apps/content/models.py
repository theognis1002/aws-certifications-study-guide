from django.db import models


QUESTION_TYPE_CHOICES = [
    ("describe_service", "describe_service"),
    ("choose_service", "choose_service"),
    ("services", "services"),
    ("billing", "billing"),
    ("general", "general"),
]


class Service(models.Model):
    service = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.service


class MultipleChoiceQuestion(models.Model):
    question = models.TextField()
    choice1 = models.TextField(blank=True, null=True)
    choice2 = models.TextField(blank=True, null=True)
    choice3 = models.TextField(blank=True, null=True)
    choice4 = models.TextField(blank=True, null=True)
    answers = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.question