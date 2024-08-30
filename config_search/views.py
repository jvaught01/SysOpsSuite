from django.shortcuts import render
from Backups.models import Backup
import logging as log

def config_search_view(request):
    query = request.GET.get('q')
    backups = Backup.objects.all()
    log.debug(backups)
    
    if query:
        # Example: Search by switch name or status, adjust as needed
        backups = backups.filter(switch_name__icontains=query) | backups.filter(backup_status__icontains=query)
    return render(request, 'config_search.html', {'backups': backups})