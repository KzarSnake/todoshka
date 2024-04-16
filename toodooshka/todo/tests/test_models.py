import datetime as dt

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Todo

User = get_user_model()


class TodoModelTest(TestCase):
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

    def test_post_str(self):
        """Выводит title при использовании str."""
        self.assertEqual(str(self.todo), self.todo.title)
