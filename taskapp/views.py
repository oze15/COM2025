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
import datetime


# is @login_required needed?
def is_admin(user):
    return user.groups.filter(name='TasksAdminUsers').exists() or user.is_superuser

# Create your views here.
@login_required
def index_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    context["today"] = datetime.date.today()
    
    if is_admin(request.user):
        context["task_list"] = Task.objects.all()
        context["task_count"] = Task.objects.all().count
    else:
        context["task_list"] = Task.objects.filter(author=request.user)
        context["task_count"] = Task.objects.filter(author=request.user).count()

    return render(request, "taskapp/index.html", context)

@login_required
def create_view(request):
    context = {}
    form = TaskForm(request.POST or None, initial={'author': request.user})
    if(request.method == 'POST'):
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Task Created')
            return redirect('tasks_index')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Task not created')

    context['form'] = form
    return render(request, "taskapp/create_view.html", context)

@login_required
def update_view(request, nid):
    context = {}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = nid)

    if(obj.author != request.user and not(is_admin(request.user))):
        raise PermissionDenied()
    
    # pass the object as instance in form
    form = TaskForm(request.POST or None, instance = obj)
    
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Task Updated')

        return redirect('tasks_detail', pk = nid)
    
    # add form dictionary to context
    context["form"] = form
    
    return render(request, "taskapp/update_view.html", context)

@login_required
def delete_view(request, nid):
    # fetch the object related to passed id
    obj = get_object_or_404(Task, id = nid)

    if(obj.author != request.user and not(is_admin(request.user))):
        raise PermissionDenied()

    # delete object
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Task Deleted')
    # after deleting redirect to index view
    return redirect('tasks_index')


class CreateSubTaskView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm

    template_name = "taskapp/create_view.html"
    
    def get_initial(self): # set the initial value of our task field
        task = Task.objects.get(id=self.kwargs['nid'])
        if(self.request.user != task.author and not(is_admin(self.request.user))):
            raise PermissionDenied()
            
        return {'task': task}
        
    
    def get_success_url(self): # redirect to the task detail view on success
        return reverse_lazy('tasks_detail', kwargs={'pk':self.kwargs['nid']})

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'taskapp/detail_view.html'
    
    def get_context_data(self, **kwargs):

        task = Task.objects.get(id=self.kwargs['pk']) 

        context = {}
        context['task'] = task

        if(self.request.user == task.author or is_admin(self.request.user)):
            
            #  get all the subtasks associated with that task
            context['subtask_list'] = SubTask.objects.filter(task__id=self.kwargs['pk'])
            context['subtask_list_size'] = SubTask.objects.filter(task__id=self.kwargs['pk']).count
        else:
            raise PermissionDenied()

        #  return a context dictionary containing this information
        return context

class CompleteSubTaskView(LoginRequiredMixin, View):
    def get(self, request):
        # Get the subtask id from the get parameters
        tid = request.GET.get('subtask_id')
        subtask = get_object_or_404(SubTask, pk=tid)

        task = subtask.task

        if(self.request.user != task.author and not(is_admin(self.request.user))):
            raise PermissionDenied()

        # Get the subtask and toggle completion
        subtask.complete = not(subtask.complete)
        subtask.save()
        # Send a JSON response
        return JsonResponse({'complete': subtask.complete, 'tid': tid}, status=200)

class DeleteSubTaskView(LoginRequiredMixin, View):
    def get(self, request):
        # Get the subtask id from the get parameters
        tid = request.GET.get('subtask_id')
        try:
            subtask = SubTask.objects.get(pk=tid)

            task = subtask.task

            if(self.request.user != task.author and not(is_admin(self.request.user))):
                raise PermissionDenied()
            
        except SubTask.DoesNotExist:
            # Get the subtask and fail gracefully if not
            return JsonResponse({'delete_success': False, 'tid': tid}, status=200)
        subtask.delete()
        # Send a JSON response on deletion
        return JsonResponse({'delete_success': True, 'tid': tid}, status=200)