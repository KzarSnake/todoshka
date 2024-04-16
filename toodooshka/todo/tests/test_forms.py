import datetime as dt

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Todo

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Автор')
        cls.todo = Todo.objects.create(
            title='Фикстура-тудушка',
            memo='Тестовая задача',
            created=dt.datetime.now(),
            user=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_todo_create_in_database(self):
        """Валидная форма создаёт запись в базе."""
        all_todo = len(Todo.objects.filter(user=self.user))

        form_data = {
            'title': 'Созданная тудушка',
            'memo': 'Эта тудушка создана через тесты',
            'created': dt.datetime.now(),
            'user': self.user,
        }
        response = self.authorized_client.post(
            reverse('createtodo'), data=form_data, follow=True
        )

        self.assertGreater(len(response.context['todos']), all_todo)
        self.assertTrue(
            Todo.objects.filter(
                title=form_data['title'],
                memo=form_data['memo'],
                user=self.user,
            ).exists()
        )
