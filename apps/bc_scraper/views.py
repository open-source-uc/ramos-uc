from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from . import tasks
from datetime import datetime
from pytz import timezone


@staff_member_required
def schedule(request):
    if request.method == "POST":
        action = request.POST.get("action")
        period = request.POST.get("period")
        banner = request.POST.get("banner")
        time = datetime.strptime(request.POST.get("time"), "%Y-%m-%dT%H:%M")
        time = timezone(settings.TIME_ZONE).localize(time)

        if action == "collect":
            tasks.collect_task(period, schedule=time)
        elif action == "update":
            tasks.update_task(period, schedule=time)
        elif action == "delete":
            tasks.delete_task(schedule=time)
        elif action == "banner":
            tasks.banner_task(period, banner, schedule=time)

    return render(request, "scraper/schedule.html", {})
