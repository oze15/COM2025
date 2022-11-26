from django.http import HttpResponse
from django.shortcuts import (get_object_or_404, render, redirect)
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
def index_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # add the dictionary during initialization
    context["task_list"] = Task.objects.all()
    
    return render(request, "taskapp/index.html", context)

# pass id attribute from urls
def detail_view(request, nid):
    
    context = {}
    
    # add the dictionary during initialization
    context["task"] = get_object_or_404(Task, pk=nid)
    
    return render(request, "taskapp/detail_view.html", context)

def create_view(request):
    context ={}
    form = TaskForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Task Created')
            return redirect('tasks_index')
        # elif Task.objects.filter(title=title).exists():
        #     messages.add_message(request, messages.ERROR, 'Task with this Title already exists')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Task not created')

    context['form']= form
    return render(request, "taskapp/create_view.html", context)

def update_view(request, nid):
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = nid)
    
    # pass the object as instance in form
    form = TaskForm(request.POST or None, instance = obj)
    
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Task Updated')

        return redirect('tasks_detail', nid=nid)
    
    # add form dictionary to context
    context["form"] = form
    
    return render(request, "taskapp/update_view.html", context)


def delete_view(request, nid):
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = nid)
    # delete object
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Task Deleted')
    # after deleting redirect to index view
    return redirect('tasks_index')
