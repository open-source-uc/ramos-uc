from django.contrib import admin
from .models import Course, Section


class SectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "period")
    list_filter = ("period", "course__school", "course__category")
    search_fields = ("course__initials",)


# Register your models here.
admin.site.register(Course)
admin.site.register(Section, SectionAdmin)
