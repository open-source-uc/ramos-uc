from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Calification
from apps.courses_calification.models import Course
from rest_framework import serializers
from django.core.cache import cache


class CalificationSearializer(serializers.Serializer):
    year = serializers.IntegerField(min_value=1900, max_value=2200, required=True)
    semester = serializers.IntegerField(min_value=1, max_value=2, required=True)
    like = serializers.IntegerField(min_value=1, max_value=5, required=True)
    difficulty = serializers.IntegerField(min_value=1, max_value=5, required=True)
    communication = serializers.IntegerField(min_value=1, max_value=5, required=True)
    credits = serializers.IntegerField(min_value=1, max_value=50, required=True)
    comment = serializers.CharField(max_length=500, required=False, default=None)


@login_required
def new(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "courses/calificate.html", {"course": course})


@login_required
def create(request, course_id):
    # validate request
    course = get_object_or_404(Course, pk=course_id)
    serializer = CalificationSearializer(data=request.POST)
    if not serializer.is_valid():
        return render(
            request,
            "courses/calificate.html",
            {
                "course": course,
                "errors": serializer.errors,
            },
        )
    params = serializer.validated_data

    # get previous calification if exists
    try:
        cal = Calification.objects.get(user=request.user, course=course)
    except Calification.DoesNotExist:
        cal = Calification(user=request.user, course=course)

    # save
    cal.period = f"{params['year']}-{params['semester']}"
    cal.like = params["like"]
    cal.difficulty = params["difficulty"]
    cal.communication = params["communication"]
    cal.credits = params["credits"]
    cal.comment = params["comment"]
    cal.save()

    # devalidate cache of course period
    cache.delete(f"s_{course.initials}_{cal.period}")

    return redirect("courses:course", initials=course.initials)
