from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length = 128, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length = 128)
    status = models.CharField(max_length = 128)
    due_at = models.DateField(blank=True, editable=True)

    class Meta:
        indexes = [models.Index(fields=['title']), ]