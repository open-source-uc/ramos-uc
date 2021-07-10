from django.db import models
from .course import Course
import re


class SectionQuerySet(models.QuerySet):
    numbers = re.compile(r"^\d{1,4}$")
    sigla = re.compile(r"^[a-zA-Z]{1,3}(\d{3,4}[a-zA-Z]?|\d{0,4})$")

    def search(self, query):
        # case numeric query
        if self.numbers.match(query):
            return self.filter(course__initials__contains=query)

        # case initials query
        elif self.sigla.match(query):
            return self.filter(course__initials__istartswith=query)

        # general case, name or teacher matches
        return self.filter(
            models.Q(course__name__unaccent__icontains=query)
            | models.Q(teachers__unaccent__icontains=query)
        )


class SectionManager(models.Manager):
    def get_queryset(self):
        return SectionQuerySet(self.model, using=self._db)

    def available(self, column_name, desc=False):
        sorted_name = "-" + column_name if desc else column_name
        values = self.distinct(column_name).order_by(sorted_name).values(column_name)
        return [x[column_name] for x in values]


class Section(models.Model):
    # Una seccion tiene:
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.CharField(max_length=6)
    section = models.PositiveSmallIntegerField()
    nrc = models.CharField(max_length=10, blank=True, null=True)

    teachers = models.CharField(max_length=1000, blank=True, null=True)
    schedule = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=16, blank=True, null=True)
    campus = models.CharField(max_length=32, blank=True, null=True)

    is_english = models.BooleanField()
    is_removable = models.BooleanField()
    is_special = models.BooleanField()

    available_quota = models.SmallIntegerField(blank=True, null=True)
    total_quota = models.SmallIntegerField(blank=True, null=True)

    objects = SectionManager()

    class Meta:
        indexes = [
            models.Index(fields=["period", "course"]),
            models.Index(fields=["course", "section"]),
            models.Index(fields=["campus"]),
            models.Index(fields=["available_quota"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["period", "course", "section"], name="period_section"
            )
        ]

    def __str__(self):
        return str(self.course.initials) + "-" + str(self.section)

    def quota_list(self):
        return list(
            self.quota_set.all()
            .order_by("date")
            .values("date", "category", "quota", "banner")
        )

    def last_quota(self):
        return self.quota_set.extra(
            where=["date=(SELECT MAX(date) FROM courses_quota WHERE section_id=%s)"],
            params=[self.id],
        ).values("date", "category", "quota")
