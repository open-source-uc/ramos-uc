from django.db import models
from django.db.models import Count, Avg


class CoursesManager(models.Manager):
    def available(self, column_name, desc=False):
        sorted_name = "-" + column_name if desc else column_name
        values = self.distinct(column_name).order_by(sorted_name).values(column_name)
        return [x[column_name] for x in values]


class Course(models.Model):
    # Un ramo tiene:
    initials = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=255)

    credits = models.PositiveSmallIntegerField()
    req = models.TextField(max_length=1000, blank=True, null=True)
    con = models.CharField(max_length=16, blank=True, null=True)
    restr = models.TextField(max_length=1000, blank=True, null=True)
    program = models.TextField(blank=True, null=True)

    school = models.CharField(max_length=32, blank=True, null=True)
    area = models.CharField(max_length=32, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)

    objects = CoursesManager()

    class Meta:
        indexes = [
            models.Index(fields=["req"]),
            models.Index(fields=["school"]),
            models.Index(fields=["area"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.initials + " - " + self.name

    def get_description(self):
        if not self.program:
            return "Descripción no disponible"
        start_description = self.program.find("DESCRIP")
        if start_description != -1:
            start_description = self.program.find("\n", start_description)
            end_description = self.program.find("II", start_description)
            return self.program[start_description:end_description]
        else:
            return "Descripción no disponible"

    def get_calification(self, period=None):
        qs = self.calification_set
        if period is not None:
            qs = qs.filter(period=period)
        return qs.aggregate(
            Avg("like"),
            Avg("load"),
            Avg("communication"),
            Avg("credits"),
            Count("like"),
        )

    def get_comments(self):
        return (
            self.calification_set.exclude(comment=None)
            .values("comment", "period", "user__username")
            .order_by("period")[:15]
        )
