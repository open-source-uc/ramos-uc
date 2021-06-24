from django.db import models
from django.conf import settings


class Comment(models.Model):
    message = models.CharField(max_length=1500)
    timestamp = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user) + ': ' + self.message
