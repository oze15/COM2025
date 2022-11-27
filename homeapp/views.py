from multiprocessing import context
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import ContactForm, UserCreationWithEmailForm
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.models import User
from taskapp.models import Task
import datetime

# Create your views here.
def home(request):
    context = {}

    context["task_list"] = Task.objects.all()
    context["task_count"] = Task.objects.all().count
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