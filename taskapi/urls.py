from django.urls import path
from .views import JWTLoginView, UserTasksView, TaskStatusUpdateView, TaskReportView

urlpatterns = [
    path('login/', JWTLoginView.as_view(), name='jwt_login'),
    path('tasks/', UserTasksView.as_view(), name='user-tasks'),
    path('task_update/<int:pk>/', TaskStatusUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]