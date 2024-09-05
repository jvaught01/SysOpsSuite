from django.shortcuts import render
from Backups.models import Backup
import logging as log


def config_search_view(request):
    backups = Backup.objects.all()
    log.debug(backups)

    if backups:
        return render(request, "config_search.html", {"results": backups})
    else:
        return render(request, "config_search.html", {"results": None})
