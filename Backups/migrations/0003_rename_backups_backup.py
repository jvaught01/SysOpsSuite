# Generated by Django 5.1 on 2024-08-27 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backups', '0002_rename_backupdata_backups'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Backups',
            new_name='Backup',
        ),
    ]
