# Generated by Django 4.1.1 on 2022-12-01 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0004_task_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
