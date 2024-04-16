from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TodoForm
from .models import Todo


def home(request):
    """Загрузка домашней страницы."""
    return render(request, 'todo/home.html')


def signupuser(request):
    """Загрузка страницы регистрации пользователя."""
    if request.method == 'GET':
        return render(
            request, 'todo/signupuser.html', {'form': UserCreationForm()}
        )
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'],
                )
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(
                    request,
                    'todo/signupuser.html',
                    {
                        'form': UserCreationForm(),
                        'error': 'Это имя пользователя занято',
                    },
                )
        else:
            return render(
                request,
                'todo/signupuser.html',
                {'form': UserCreationForm(), 'error': 'Пароли не совпадают!'},
            )


def loginuser(request):
    """Загрузка страницы авторизации пользователя."""
    if request.method == 'GET':
        return render(
            request, 'todo/loginuser.html', {'form': AuthenticationForm()}
        )
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is None:
            return render(
                request,
                'todo/loginuser.html',
                {
                    'form': AuthenticationForm(),
                    'error': 'Логин и пароль не совпадают',
                },
            )
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    """Загрузка страницы выхода пользователя."""
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    """Загрузка страницы и создание новой задачи."""
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/createtodo.html',
                {'form': TodoForm(), 'error': 'Передана неверная информация'},
            )


@login_required
def currenttodos(request):
    """Загрузка страницы с текущими задачами."""
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    """Загрузка страницы с завершенными задачами."""
    todos = Todo.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    """Загрузка страницы выбранной задачи."""
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(
            request, 'todo/viewtodo.html', {'todo': todo, 'form': form}
        )
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/viewtodo.html',
                {'todo': todo, 'form': form, 'error': 'Неверные данные'},
            )


@login_required
def completetodo(request, todo_pk):
    """Обработка нажатия кнопки завершения задачи."""
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    """Обработка нажатия кнопки удаления задачи."""
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
