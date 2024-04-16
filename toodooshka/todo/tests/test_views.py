import datetime as dt

from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import TodoForm
from ..models import Todo

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор')
        cls.todo = Todo.objects.create(
            title='Текущая тудушки',
            memo='Тестовая задача',
            created=dt.datetime.now(),
            user=cls.user,
        )
        cls.complete_todo = Todo.objects.create(
            title='Завершенная тудушка',
            memo='Тестовая готовая задача',
            created=dt.datetime.now(),
            datecompleted=dt.datetime.now(),
            user=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('home'): 'todo/home.html',
            reverse('signupuser'): 'todo/signupuser.html',
            reverse('loginuser'): 'todo/loginuser.html',
            reverse('createtodo'): 'todo/createtodo.html',
            reverse('currenttodos'): 'todo/currenttodos.html',
            reverse('completedtodos'): 'todo/completedtodos.html',
            reverse('viewtodo', args=[self.todo.id]): 'todo/viewtodo.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_current_and_completed_pages_show_correct_context(self):
        """Шаблон current и completed сформированы со списками записей."""
        testing_todo_pages = {
            reverse('currenttodos'): self.todo,
            reverse('completedtodos'): self.complete_todo,
        }
        for reverse_name, todo in testing_todo_pages.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                test_todo = response.context.get('todos')[0]
                self.assertEqual(todo, test_todo)

    def test_createtodo_show_correct_context(self):
        """Шаблон createtodo сформирован с правильной формой."""
        response = self.authorized_client.get(reverse('createtodo'))
        form_fields = {
            'title': forms.fields.CharField,
            'memo': forms.fields.CharField,
            'important': forms.fields.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)
                self.assertTrue('form' in response.context)
                self.assertIsInstance(response.context['form'], TodoForm)

    def test_new_and_complete_todo_added_right_pages(self):
        """
        Новая запись появляется на странице текущих задач,
        завершенная задача появляется на странице завершенных задач.
        """
        new_todo = Todo.objects.create(
            title='Новая тудушка',
            memo='Текст новосозданной тудушки',
            created=dt.datetime.now(),
            user=self.user,
        )
        new_complete_todo = Todo.objects.create(
            title='Завершенная тудушка',
            memo='Тестовая готовая задача',
            created=dt.datetime.now(),
            datecompleted=dt.datetime.now(),
            user=self.user,
        )
        testing_todo_pages = {
            reverse('currenttodos'): new_todo,
            reverse('completedtodos'): new_complete_todo,
        }
        for reverse_name, todo in testing_todo_pages.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIn(todo, response.context['todos'])

    def test_new_todo_not_in_wrong_pages(self):
        """
        Новая запись не появляется на странице завершенных задач,
        завершенная задача не появляется на странице текущих задач.
        """
        new_todo = Todo.objects.create(
            title='Новая тудушка',
            memo='Текст новосозданной тудушки',
            created=dt.datetime.now(),
            user=self.user,
        )
        new_complete_todo = Todo.objects.create(
            title='Завершенная тудушка',
            memo='Тестовая готовая задача',
            created=dt.datetime.now(),
            datecompleted=dt.datetime.now(),
            user=self.user,
        )
        testing_todo_pages = {
            reverse('currenttodos'): new_complete_todo,
            reverse('completedtodos'): new_todo,
        }
        for reverse_name, todo in testing_todo_pages.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertNotIn(todo, response.context['todos'])
