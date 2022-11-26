from django import forms
from .models import Task
# creating a form

class TaskForm(forms.ModelForm):
    # create meta class

    class Meta:
    # specify model to be used
        model = Task
        
        fields = ['title', 'description', 'due_at']

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

            'due_at': forms.SelectDateWidget(attrs={
            'class': 'form-control',
            # 'placeholder': 'Task Title',
            }),

}