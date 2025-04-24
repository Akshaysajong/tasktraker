from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Task, UserProfile, User
from .form import TaskForm, UserCreateForm, UserUpdateForm, TaskUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import superadmin_required, admin_required

@admin_required
@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'dashboard.html')

def login_user(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return redirect("dashboard")
        else:
            messages.error(request, "Username or Password is incorrect !")
            return redirect("login_user")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

@admin_required
@login_required(login_url="/login/")
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            print("=================")
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('tasklist')
    else:
        form = TaskForm()
    return render(request, 'addtasks.html', {'form': form})

@admin_required
@login_required(login_url="/login/")
def tasklist(request):
    task = Task.objects.all()
    return render(request, 'tasklist.html', {'task':task})

@admin_required
@login_required(login_url="/login/")
def userlist(request):
    current_user = request.user
    excluded_users = UserProfile.objects.filter(user_type='superadmin').values_list('user_id', flat=True)
    print("excluded_users:", excluded_users)
    users = User.objects.exclude(id__in=excluded_users).exclude(id=current_user.id)
    return render(request, 'userlist.html',{'user':users})

@superadmin_required
@login_required(login_url="/login/")
def adduser(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlist')
    else:
        form = UserCreateForm()
    return render(request, 'adduser.html', {'form': form})

@superadmin_required
@login_required(login_url="/login/")
def updateuser(request):
    user_id = request.GET['a']
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userlist') 
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'updateuser.html', {'form': form})

@superadmin_required
@login_required(login_url="/login/")
def removeuser(request):
    id = request.GET['a']
    User.objects.filter(id=id).delete()
    return redirect('userlist')

@admin_required
@login_required(login_url="/login/")
def edittask(request):
    task_id = request.GET['a']
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, 'edittask.html', {'form': form, 'task': task})