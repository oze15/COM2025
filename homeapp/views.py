from multiprocessing import context
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import ContactForm, UserCreationWithEmailForm
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.models import User
from taskapp.models import Task
import datetime

def is_admin(user):
    return user.groups.filter(name='TasksAdminUsers').exists() or user.is_superuser

def is_auth(user):
    return user.is_authenticated

def is_anon(user):
    return user.is_anonymous

# Create your views here.

def home(request):
    context = {}
    # if is_auth == True:

    context["task_list"] = 0
    context["task_count"] = 0

    context["task_count_delayed"] = 0
    context["task_count_in_progress"] = 0
    context["task_count_urgent"] = 0
    context["task_count_not_started"] = 0

    if is_admin(request.user):

        filterObjects = Task.objects
        allObjects = filterObjects.all()

        task_delayed = filterObjects.filter(status = 'Delayed')
        task_in_progress = filterObjects.filter(status = 'In progress')
        task_urgent = filterObjects.filter(status = 'Urgent')
        # task_not_started = filterObjects.exclude(task_in_progress)
        task_not_started = filterObjects.filter(status = 'Not started')

        context["task_list"] = Task.objects.all()
        context["task_count"] = Task.objects.all().count

        context["task_list"] = allObjects
        context["task_count"] = allObjects.count

        context["task_count_delayed"] = task_delayed.count
        context["task_count_in_progress"] = task_in_progress.count
        context["task_count_urgent"] = task_urgent.count
        context["task_count_not_started"] = task_not_started.count
    else:
        context["task_list"]    = Task.objects.filter(author=request.user.id)
        context["task_count"]   = Task.objects.filter(author=request.user.id).count()

        task_count_delayed_u        = Task.objects.filter(author=request.user.id, status = 'Delayed')
        task_count_in_progress_u    = Task.objects.filter(author=request.user.id, status = 'In progress')
        task_count_urgent_u         = Task.objects.filter(author=request.user.id, status = 'Urgent')
        task_count_not_started_u    = Task.objects.filter(author=request.user.id, status = 'Not started')

        context["task_count_delayed"]       = task_count_delayed_u.count
        context["task_count_in_progress"]   = task_count_in_progress_u.count
        context["task_count_urgent"]        = task_count_urgent_u.count
        context["task_count_not_started"]   = task_count_not_started_u.count


    context["today"] = datetime.date.today()

    return render(request, 'homeapp/home.html', context)

def contact(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = name + ':\n' + form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['myemail@mydomain.com'])
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message Not Sent')
                return HttpResponse("Invalid header found.")
            messages.add_message(request, messages.SUCCESS, 'Message Sent')
            return redirect(reverse('home'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Message Not Sent') 

    return render(request, 'homeapp/contact.html', {"form": form})

class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'homeapp/register.html'
    
    success_url = reverse_lazy('login')