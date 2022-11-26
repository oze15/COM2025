from django.urls import path
from . import views

urlpatterns = [
    # tasks/
    path('', views.index_view, name='tasks_index'),
    # tasks/id
    path('<int:pk>', views.TaskDetailView.as_view(), name='tasks_detail'),
    # tasks/new
    path('new', views.create_view, name='tasks_new'),
    # tasks/edit/id
    path('edit/<int:nid>', views.update_view, name='tasks_update'),
    # tasks/delete/id
    path('delete/<int:nid>', views.delete_view, name='tasks_delete'),
    #tasks/id/subtasks/
    # path('<int:nid>/subtasks', views.SubTaskListView.as_view(), name='subtask_list'),
    #tasks/id/subtask/new
    path('<int:nid>/subtask/new', views.CreateSubTaskView.as_view(), name='create_subtask'),
    #/tasks/togglecomplete
    path('togglecomplete', views.CompleteSubTaskView.as_view(), name='complete_subtask'),
    #/tasks/deletesubtask
    path('deletesubtask', views.DeleteSubTaskView.as_view(), name='delete_subtask'),
]
