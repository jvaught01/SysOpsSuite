from django import template
from tasks.models import Task

register = template.Library()

@register.filter
def first_name_from_email(email):
    if email:
        # Split email by '@', take the first part, then split by '.', and capitalize the first name
        first_part = email.split('@')[0].split('.')[0]
        return first_part.capitalize()
    return ''

@register.filter
def get_completed_tasks(user):
    queryset = Task.objects.filter(created_by=user, completed=True)
    if queryset.count() == 0:
        return '0'
    return queryset.count()