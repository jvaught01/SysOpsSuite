from django.shortcuts import render
from .models import Backup
import logging as log

def backups_view(request):
    backups = Backup.objects.all()
    log.debug(backups)
    return render(request, 'backups.html', {'backups': backups})