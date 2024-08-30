from django.shortcuts import render
from .models import Task
from django.shortcuts import get_object_or_404, redirect


def tasks_view(request):
    tasks = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        if request.POST.get('title'):
            task.title = request.POST.get('title')
        if request.POST.get('due_date'):
            task.due_date = request.POST.get('due_date')
        if request.POST.get('description'):
            task.description = request.POST.get('description')
        task.save()
        return redirect('task_list')  # Adjust this as needed
    return redirect('task_list')  # Fallback

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')