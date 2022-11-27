from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name')
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}), label='Email address')
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Brief description')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label='What would you like to change?')

class UserCreationWithEmailForm(UserCreationForm):

    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email")
