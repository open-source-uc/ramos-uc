from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Course, Section
from .serializers import PlannerSearchSerializer
from django.views.decorators.cache import cache_control, never_cache
from django.core.cache import cache
from django.core.paginator import Paginator
import re


# Home
def home(request):
    return render(request, "index.html")


def get_fields_values():
    return {
        "mods": ["8:30", "10:00", "11:30", "2:00", "3:30", "5:00", "6:30", "8:00"],
        "schools": Course.objects.available("school"),
        "campuses": Section.objects.available("campus"),
        "formats": Section.objects.available("format"),
        "categories": Course.objects.available("category"),
        "areas": Course.objects.available("area"),
    }


# Planner index
@cache_control(private=True, max_age=3600 * 12)
def planner(request):
    data = cache.get_or_set("possible_values", get_fields_values, 3600 * 12)
    return render(request, "courses/planner.html", data)


# Shared schedule
@cache_control(private=True, max_age=3600 * 24)
def share(request):
    return render(
        request,
        "courses/share.html",
        {
            "mods": ["8:30", "10:00", "11:30", "2:00", "3:30", "5:00", "6:30", "8:00"],
            "ids": request.GET.get("h", []),
        },
    )


# Banner
@never_cache
def banner(request, id):
    try:
        section = Section.objects.get(pk=id)
    except Section.DoesNotExist:
        return JsonResponse({"error": "Error 404"}, status=404)
    return JsonResponse(
        {
            "initials": str(section),
            "name": section.course.name,
            "quota": section.quota_list(),
            "total_quota": section.total_quota,
        }
    )


# Planner search
@cache_control(must_revalidate=True)
def planner_search(request):
    # parse QueryDict to data dict
    data = {}
    for key in request.GET.keys():
        v = request.GET.getlist(key)
        if key[-2:] == "[]":
            key = key[:-2]
        elif v[0]:
            v = v[0]
        else:
            continue
        data[key] = v

    serializer = PlannerSearchSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors})
    params = serializer.validated_data

    # Base filter
    sections = Section.objects.filter(period=params["period"])

    # Query filter
    if len(params["q"]):
        sections = sections.search(params["q"])

    # Credits filter
    if params["credits"] is not None:
        sections = sections.filter(course__credits=params["credits"])

    # Campus filter
    if len(params["campus"]):
        sections = sections.filter(campus__in=params["campus"])

    # Format filter
    if len(params["format"]):
        sections = sections.filter(format__in=params["format"])

    # School filter
    if len(params["school"]):
        sections = sections.filter(course__school__in=params["school"])

    # Area filter
    if len(params["area"]):
        sections = sections.filter(course__area__in=params["area"])

    # Req
    if params["without_req"]:
        sections = sections.filter(course__req="No tiene")

    # Max_mod
    if params["max_mod"]:
        sections = sections.exclude(scheduleinfo__total__gt=params["max_mod"])

    # Mod_types
    if params["mod_types"]:
        disallowed_types = ["AYU", "CLAS", "LAB", "PRA", "SUP", "TAL", "TER", "TES"]
        for mod_type in params["mod_types"]:
            if mod_type == "OTRO":
                disallowed_types.remove("PRA")
                disallowed_types.remove("SUP")
                disallowed_types.remove("TES")
            else:
                disallowed_types.remove(mod_type)
        for mod_type in disallowed_types:
            column = "scheduleinfo__" + mod_type.lower() + "__gt"
            sections = sections.exclude(**{column: 0})

    # Schedule
    if params["overlap"]:
        if not params["overlap_except"]:
            for module in params["schedule"].strip().split(","):
                if module:
                    column = "fullschedule__" + module.lower()
                    sections = sections.filter(**{column: "FREE"})
        else:
            for module in params["schedule"].strip().split(","):
                if module:
                    column = "fullschedule__" + module.lower() + "__in"
                    sections = sections.filter(**{column: ["FREE", "AYU", "TER"]})

    # Category
    if len(params["category"]):
        sections = sections.filter(course__category__in=params["category"])

    # Quota
    if params["free_quota"]:
        sections = sections.exclude(available_quota=0)

    # Paginate an create response
    results = []
    start = (params["page"] - 1) * 25
    for s in sections[start : start + 25]:
        results.append(
            {
                "id": s.id,
                "initials": str(s),
                "name": s.course.name,
                "teachers": s.teachers,
                "format": s.format,
                "available_quota": s.available_quota,
                "schedule": s.schedule,
                "course_initials": str(s).split("-")[0],
                "section": int(str(s).split("-")[1]),
            }
        )
    return JsonResponse({"results": results})


# Course profile
@cache_control(private=True, max_age=3600 * 12)
def single_course(request, initials):
    initials = initials.upper()
    period = request.GET.get("period")

    # Get course data
    cached_course = cache.get("c_" + initials)
    if cached_course is None:
        course = get_object_or_404(Course, initials=initials)
        # Link requirements
        requirements = (
            re.sub(
                r"([a-zA-Z]{3}\d{3,4}[a-zA-Z]?)",
                r'<a href="/ramo/\1">\1</a>',
                course.req,
            )
            if course.req
            else "No tiene"
        )
        program = (
            course.program.replace("\\", "<br>").replace("\n", "<br>")
            if course.program
            else "No disponible"
        )
        cached_course = {
            "course": course,
            "program": program,
            "description": course.get_description(),
            "requirements": requirements,
            "periods": course.section_set.available("period", desc=True),
            "calification": course.get_calification(),
        }
        cache.set("c_" + initials, cached_course, 3600 * 24)

    # Get sections data
    if period is None:
        period = cached_course["periods"][0] if len(cached_course["periods"]) else ""
    cached_sections = cache.get(f"s_{initials}_{period}")
    if cached_sections is None:
        course = get_object_or_404(Course, initials=initials)
        cached_sections = {
            "sections": course.section_set.filter(period=period).order_by("section"),
            "period": period,
        }
        cache.set(f"s_{initials}_{period}", cached_sections, 3600 * 12)

    # Send response
    return render(request, "courses/course.html", {**cached_course, **cached_sections})


# Section detail on planner
@cache_control(must_revalidate=True)
def single_section(request, id):
    try:
        section = Section.objects.get(pk=id)
    except Section.DoesNotExist:
        return JsonResponse({"error": "Error 404"}, status=404)
    course = section.course
    quota = section.last_quota()
    return JsonResponse(
        {
            "initials": str(section),
            "name": course.name,
            "is_removable": section.is_removable,
            "is_english": section.is_english,
            "is_special": section.is_special,
            "campus": section.campus,
            "credits": course.credits,
            "school": course.school,
            "area": course.area,
            "category": course.category,
            "format": section.format,
            "teachers": section.teachers,
            "req": course.req,
            "con": course.con,
            "restr": course.restr,
            "url": reverse("courses:course", args=[course.initials]),
            "quota": list(quota),
            "total_quota": section.total_quota,
            "available_quota": section.available_quota,
        }
    )


# Data to add section to schedule
@cache_control(private=True, max_age=3600 * 24)
def schedule(request, id):
    try:
        section = Section.objects.get(pk=id)
    except Section.DoesNotExist:
        return JsonResponse({"error": "Error 404"}, status=404)
    schedule = section.fullschedule.__dict__
    schedule.pop("_state")
    schedule.pop("section_id")
    clean_schedule = {}
    for key in schedule:
        if schedule[key] != "FREE":
            clean_schedule[key] = schedule[key]

    return JsonResponse(
        {
            "initials": str(section),
            "name": section.course.name,
            "period": section.period,
            "schedule": clean_schedule,
        }
    )


# Browse
@cache_control(private=True, max_age=3600 * 24)
def browse(request):
    school_name = request.GET.get("escuela", None)

    # Case single school
    if school_name is not None:
        courses = Course.objects.filter(school=school_name).order_by("initials")
        paginator = Paginator(courses, 50)
        page_number = request.GET.get("page")
        return render(
            request,
            "courses/school.html",
            {
                "courses_page": paginator.get_page(page_number),
                "school_name": school_name,
            },
        )

    data = cache.get_or_set("possible_values", get_fields_values, 3600 * 12)
    return render(request, "courses/browse.html", data)


# Search
@cache_control(private=True, max_age=3600)
def search(request):
    q = request.GET.get("q", "")
    results = Section.objects.all().search(q).distinct("course_id")[:20]
    return render(
        request,
        "courses/search.html",
        {
            "results": results,
            "q": q,
            "results_count": len(results),
        },
    )


# Crea
@cache_control(must_revalidate=True)
def create(request):
    data = cache.get_or_set("possible_values", get_fields_values, 3600 * 12)
    return render(request, "courses/create.html", data)
