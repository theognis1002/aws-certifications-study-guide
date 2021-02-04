from django.db import models


CERT_TYPE_CHOICES = [
    ("aws_cloud_practitioner", "AWS Cloud Practitioner"),
    ("aws_developer", "AWS Certified Developer"),
    ("aws_solutions_architect_associate", "AWS Solutions Architect Associate"),
]


class Service(models.Model):
    service = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.service


class MultipleChoiceQuestion(models.Model):
    cert_type = models.CharField(
        max_length=255, choices=CERT_TYPE_CHOICES, default=CERT_TYPE_CHOICES[0][0]
    )
    question = models.TextField()
    choice1 = models.TextField(blank=True, null=True)
    choice2 = models.TextField(blank=True, null=True)
    choice3 = models.TextField(blank=True, null=True)
    choice4 = models.TextField(blank=True, null=True)
    answers = models.CharField(max_length=255)
    reference = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.question