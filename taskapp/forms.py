from django import forms
from .models import Task
# creating a form

Category_Choices = [
    'Not started',
    'Delayed',
    'Urgent',
    'In progress',
    'Complete',
]

Status_Choices = [
    'Not started',
    'Delayed',
    'Urgent',
    'In progress',
    'Complete',
]

class TaskForm(forms.ModelForm):
    # create meta class

    class Meta:
    # specify model to be used
        model = Task
        
        fields = ['title', 'description', 'category',  'status', 'due_at']

        widgets = {
            
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Task Title',
            }),
            
            'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Task Description',
            'rows' : 15,
            'cols' : 60,
            }),

            'category': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category',
            }),

            'status': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Status',
            }),

            'due_at': forms.SelectDateWidget(attrs={
            'class': 'form-control',
            # 'placeholder': 'Task Title',
            }),



}