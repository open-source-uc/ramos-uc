from django.urls import path
from . import views


app_name = "courses"
urlpatterns = [
    # Home
    path("", views.home, name="index"),
    # Planner
    path("planifica", views.planner, name="planner"),
    path("p_search", views.planner_search, name="p_search"),
    path("detalle/<int:id>", views.single_section, name="p_detail"),
    path("detalle/<int:id>/horario", views.schedule, name="p_schedule"),
    # Banner
    path("banner/<int:id>", views.banner, name="banner"),
    # Shared schedule
    path("share", views.share, name="share"),
    # Courses info
    path("ramo/<str:initials>", views.single_course, name="course"),
    # Browse courses by school
    path("ramos", views.browse, name="browse"),
    # Search
    path("buscar", views.search, name="search"),
]
