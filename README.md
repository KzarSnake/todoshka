# Приложение Тудушка - простой список дел

## Описание
Простой список дел с системой авторизации. Зарегистрированный пользователь может:
- создать задачу;
- завершить ранее созданную задачу;
- просмотреть список текущих задач;
- посмотреть текущую задачу подробнее;
- просмотреть список завершенных задач;
- удалить задачу.

## Стэк технологий:

- Python 3.10
- Django 3.2
- SQLite3

## Подготовка к запуску:

**Клонируйте репозиторий:**

```
git clone git@github.com:KzarSnake/toodooshka.git
```

**Установите и активируйте виртуальное окружение:**

```
python -m venv venv
source venv/Scripts/activate
```

**Установите зависимости из файла requirements.txt:**

```
pip install -r requirements.txt
```

**Выполните миграции:**
```
python manage.py migrate
```

**Создайте файл .env**
Пример заполнения файла:
```
SECRET_KEY=YOUR_KEY_HERE
```

## Запуск:
Находясь в директории проекта c файлом manage.py, выполните в терминале команду:

```
python manage.py runserver
```


## Автор проекта:

[Денис Свашенко](https://github.com/KzarSnake)
