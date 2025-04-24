from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name="logout_user" ),
    path('task_create/', views.task_create, name='addtask'),
    path('tasklist/', views.tasklist, name='tasklist'),
    path('userlist/', views.userlist, name='userlist'),
    path('adduser/', views.adduser, name='adduser'),
    path('updateuser/', views.updateuser, name='updateuser'),
    path('removeuser/', views.removeuser, name='removeuser'),
    path('edittask/', views.edittask, name='edittask'),
]