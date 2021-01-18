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
