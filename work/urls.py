from django.urls import path
from . import views

app_name = 'work'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:task_pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:task_pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:task_pk>/status/', views.TaskStatusUpdateView.as_view(), name='task_status_update'),
]
