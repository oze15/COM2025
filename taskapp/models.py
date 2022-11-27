from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length = 128, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length = 128)
    status = models.CharField(max_length = 128)
    due_at = models.DateField(blank=True, editable=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # String method for a subtask will return title
    # This will make them easier to manage in the admin pages
    def __str__(self):
        return self.title

    class Meta:
        indexes = [models.Index(fields=['title']), ]

class SubTask(models.Model):
    title = models.CharField(max_length=128)
    complete = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


    # String method for a subtask will return title
    # This will make them easier to manage in the admin pages
    def __str__(self):
        return self.title