from django.db import models
from .section import Section


class Quota(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateTimeField()
    category = models.CharField(max_length=255)
    quota = models.IntegerField(blank=True, null=True)
    banner = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["section_id", "date"]),
        ]
