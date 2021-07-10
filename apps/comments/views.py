from django.shortcuts import redirect
from .models import Comment
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    message = request.POST.get("message", "").strip()
    if message:
        comment = Comment(message=message, user=request.user)
        comment.save()
    return redirect("courses:index")
