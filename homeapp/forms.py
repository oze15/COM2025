from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name')
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}), label='Email address')
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Brief description')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label='What would you like to change?')
