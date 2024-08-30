# Generated by Django 5.1 on 2024-08-27 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch_name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=50)),
                ('backup_date', models.DateField()),
                ('config_data', models.JSONField()),
                ('backup_status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
