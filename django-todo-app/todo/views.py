from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from todo.models import Task


def httpAddTask(request):
    task = request.POST['task']
    if task == '':
        return HttpResponse("Invalid data")
    Task.objects.create(task=task)
    return redirect('home')
        
def mark_As_Done(request, id):
    task = get_object_or_404(Task, id=id)
    task.is_completed = True
    task.save()
    return redirect('home')

def mark_As_Undone(request, id):
    task = get_object_or_404(Task, id=id)
    task.is_completed = False
    task.save()
    return redirect('home')

def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        new_task = request.POST['task']
        task.task = new_task
        task.save()
        return redirect('home')
    else:
        context = {
            'get_todo': task
        }
        return render(request, 'edit_task.html', context=context)

def delete_Todo(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('home')

