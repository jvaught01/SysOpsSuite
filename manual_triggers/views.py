from django.shortcuts import render


def manual_triggers(request):
    return render(request, "manual_triggers.html")
