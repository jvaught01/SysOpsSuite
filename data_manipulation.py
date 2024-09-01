import os
from datetime import datetime
import django
import logging as log

log.basicConfig(level=log.DEBUG)
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SysOpsSuite.settings")
django.setup()

from Backups.models import (  # noqa: E402
    Backup,
)  # Import your Django model here after setting up Django  # noqa: E402

# Directory containing the backups
BACKUP_DIR = "/Users/jvaught/Documents/python/projects/SYSOPSSUITE/Backups/"
switch_name = "dl2-cs1"

# Get dl2-cs1 config data from databse from data 2024-08-21
data = Backup.objects.get(switch_name=switch_name, backup_date="2024-08-21")
json_data = data.config_data

# parse json data to get the device type
Hostname = json_data["Hostname"]
Vlans = json_data["Vlans"]
Interfaces = json_data["Interfaces"]
StaticRoutes = json_data["Routing"]["StaticRoutes"]
OSPF = json_data["Routing"]["OSPF"]
BGP = json_data["Routing"]["BGP"]
EIGRP = json_data["Routing"]["EIGRP"]
ACL = json_data["ACL"]
