from django.shortcuts import render
from todo.models import Task

def home(request):
    uncompleted_tasks = Task.objects.filter(is_completed=False)
    context ={
        "uncompleted_task": uncompleted_tasks
    }
    return render(request, "home.html", context=context)