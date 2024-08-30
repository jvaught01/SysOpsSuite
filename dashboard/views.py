from django.shortcuts import render
from tasks.models import Task


def home_view(request):
    if request.user.is_authenticated:
        task = Task.objects.filter(created_by=request.user).last()
    else:
        task = None

    return render(request, "home.html", {"task": task})
