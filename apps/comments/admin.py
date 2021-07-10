from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "timestamp")


admin.site.register(Comment)
