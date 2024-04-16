import datetime as dt

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from todo.models import Todo

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор')
        cls.todo = Todo.objects.create(
            title='Название тудушки',
            memo='Тестовая задача',
            created=dt.datetime.now(),
            user=cls.user,
        )
        cls.complete_todo = Todo.objects.create(
            title='Название тудушки',
            memo='Тестовая готовая задача',
            created=dt.datetime.now(),
            datecompleted=dt.datetime.now(),
            user=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_accessible_for_guest(self):
        """Набор страниц доступен для неавторизованного пользователя."""
        testing_guest_urls = (
            reverse('home'),
            reverse('signupuser'),
            reverse('loginuser'),
        )
        for url in testing_guest_urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_accessible_for_user(self):
        """Набор страниц доступен авторизованному пользователю."""
        testing_urls = (
            reverse('home'),
            reverse('signupuser'),
            reverse('loginuser'),
            reverse('createtodo'),
            reverse('currenttodos'),
            reverse('completedtodos'),
            reverse('viewtodo', args=[self.todo.id]),
        )
        for url in testing_urls:
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_guest(self):
        """Страницы доступные для авторизованного пользователя редиректят
        гостя на страницу авторизации."""
        urls_and_redirects = {
            reverse('createtodo'): '/login/?next=/create/',
            reverse('currenttodos'): '/login/?next=/current/',
            reverse('completedtodos'): '/login/?next=/completed/',
            reverse(
                'viewtodo', args=[self.todo.id]
            ): f'/login/?next=/todo/{self.todo.id}',
            reverse('logoutuser'): '/login/?next=/logout/',
        }
        for url, redirect in urls_and_redirects.items():
            with self.subTest():
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'todo/home.html': '/',
            'todo/signupuser.html': '/signup/',
            'todo/loginuser.html': '/login/',
            'todo/createtodo.html': '/create/',
            'todo/currenttodos.html': '/current/',
            'todo/completedtodos.html': '/completed/',
            'todo/viewtodo.html': '/todo/1',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
