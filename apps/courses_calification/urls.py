from django.urls import path
from . import views


app_name = "califications"
urlpatterns = [
    path("new/<int:course_id>", views.new, name="new"),
    path("create/<int:course_id>", views.create, name="create"),
]
