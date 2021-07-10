from django.db import models
from apps.courses.models import Course
from django.conf import settings


class Calification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.CharField(max_length=6)

    load = models.PositiveSmallIntegerField()
    like = models.PositiveSmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["course", "period"]),
            models.Index(fields=["user", "period"]),
        ]
