from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import (get_object_or_404, render, redirect)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib import messages
from .models import Task, SubTask
from .forms import TaskForm, SubTaskForm
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

# Create your views here.
def index_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # add the dictionary during initialization
    context["task_list"] = Task.objects.all()
    context["task_count"] = Task.objects.all().count
    
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


class CreateSubTaskView(CreateView):
    model = SubTask
    form_class = SubTaskForm

    template_name = "taskapp/create_view.html"
    
    # wrapped in 'if' and returns
    '''
    ValueError at /tasks/13/subtask/new
    dictionary update sequence element #0 has length 0; 2 is required

    --> it does stop the user accessing subtasks that aren't their own
    '''
    def get_initial(self): # set the initial value of our task field
        task = Task.objects.get(id=self.kwargs['nid'])
        # if(self.request.user != task.author and not(is_admin(self.request.user))):
        #     raise PermissionDenied()
            
        return {'task': task}
        
    
    def get_success_url(self): # redirect to the task detail view on success
        return reverse_lazy('tasks_detail', kwargs={'pk':self.kwargs['nid']})

'''
    TypeError at /tasks/13
    context must be a dict rather than HttpResponseForbidden.

    --> followed 
    '''
class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskapp/detail_view.html'
    
    def get_context_data(self, **kwargs):

        task = Task.objects.get(id=self.kwargs['pk']) 

        context = {}
        context['task'] = task

        # get the task referred to by pk in the url
        context['subtask_list'] = SubTask.objects.filter(task__id=self.kwargs['pk'])
        # # context['task'] = Task.objects.get(id=self.kwargs['pk'])

        # if(self.request.user == task.author or is_admin(self.request.user)):
            
        #     #  get all the subtasks associated with that task
        #     context['subtask_list'] = SubTask.objects.filter(task__id=self.kwargs['pk'])
        # else:
        #     raise PermissionDenied()

        #  return a context dictionary containing this information
        return context

class CompleteSubTaskView(View):
    def get(self, request):
        # Get the subtask id from the get parameters
        tid = request.GET.get('subtask_id')
        subtask = get_object_or_404(SubTask, pk=tid)

        task = subtask.task

        # if(self.request.user != task.author and not(is_admin(self.request.user))):
        #     raise PermissionDenied()

        # Get the subtask and toggle completion
        subtask.complete = not(subtask.complete)
        subtask.save()
        # Send a JSON response
        return JsonResponse({'complete': subtask.complete, 'tid': tid}, status=200)

class DeleteSubTaskView(View):
    def get(self, request):
        # Get the subtask id from the get parameters
        tid = request.GET.get('subtask_id')
        try:
            subtask = SubTask.objects.get(pk=tid)

            task = subtask.task

            # if(self.request.user != task.author and not(is_admin(self.request.user))):
            #     raise PermissionDenied()
            
        except SubTask.DoesNotExist:
            # Get the subtask and fail gracefully if not
            return JsonResponse({'delete_success': False, 'tid': tid}, status=200)
        subtask.delete()
        # Send a JSON response on deletion
        return JsonResponse({'delete_success': True, 'tid': tid}, status=200)