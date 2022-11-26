from django.urls import path
from . import views

urlpatterns = [
    # tasks/
    path('', views.index_view, name='tasks_index'),
    # tasks/id
    path('<int:nid>', views.detail_view, name='tasks_detail'),
    # tasks/new
    path('new', views.create_view, name='tasks_new'),
    # tasks/edit/id
    path('edit/<int:nid>', views.update_view, name='tasks_update'),
    # tasks/delete/id
    path('delete/<int:nid>', views.delete_view, name='tasks_delete'),
]
