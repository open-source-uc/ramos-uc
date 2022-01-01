from django.db import models
from apps.courses.models import Course
from django.conf import settings


class Calification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.CharField(max_length=6)

    like = models.PositiveSmallIntegerField(blank=True, null=True)
    difficulty = models.PositiveSmallIntegerField(blank=True, null=True)
    credits = models.PositiveSmallIntegerField(blank=True, null=True)
    communication = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.CharField(blank=True, null=True, max_length=400)

    load = models.PositiveSmallIntegerField(blank=True, null=True)
    online_adaptation = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["course", "period"]),
            models.Index(fields=["user", "period"]),
        ]
