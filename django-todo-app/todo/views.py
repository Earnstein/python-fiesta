from django.shortcuts import redirect
from django.http import HttpResponse
from todo.models import Task
# Create your views here.

def httpAddTask(request):
    task = request.POST['task']
    if task == '':
        return HttpResponse("Invalid data")
    Task.objects.create(task=task)
    return redirect('home')
        
