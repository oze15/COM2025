from django import forms
from .models import Task, SubTask
# creating a form

Category_Choices = [
    'Not started',
    'Delayed',
    'Urgent',
    'In progress',
    'Complete',
]

STATUS_CHOICES = (
    ('Not started', 'Not started'),
    ('Delayed', 'Delayed'),
    ('Urgent', 'Urgent'),
    ('In progress', 'In progress'),
    ('Complete', 'Complete'),
)

class TaskForm(forms.ModelForm):
    # create meta class

    class Meta:
    # specify model to be used
        model = Task
        
        fields = ['title', 'description', 'category',  'status', 'due_at', 'author']

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

            'status': forms.Select(choices=STATUS_CHOICES, attrs={
            'class': 'form-control',
            }),

            'due_at': forms.SelectDateWidget(attrs={
            'class': 'form-control',
            # 'placeholder': 'Task Title',
            }),
            'author': forms.HiddenInput(),

}

# We’ll set the task id automatically depending on the url, so let’s hide that field
class SubTaskForm(forms.ModelForm):
# create meta class
    class Meta:
    # specify model to be used
        model = SubTask
        fields = ['title', 'complete', 'task']
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'formfield',
            'placeholder': 'Subtask Title',
            }),
        'task': forms.HiddenInput(),
}