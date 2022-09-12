from django.contrib.auth.models import AbstractUser
from django.db import models


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=55)
    price = models.FloatField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    subscription = models.ForeignKey(
        SubscriptionPlan, on_delete=models.DO_NOTHING, default=1
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-is_active"]


class Support(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    contact = models.EmailField()
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact} - {self.subject}"

    class Meta:
        verbose_name = "Contact messages"
        verbose_name_plural = "Contact messages"
