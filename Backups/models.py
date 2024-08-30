from django.db import models


class Backup(models.Model):
    switch_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    backup_date = models.DateField()
    config_data = models.JSONField()
    backup_status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.switch_name
    