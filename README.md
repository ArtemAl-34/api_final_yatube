▎Название проекта

api_yatube

▎Описание проекта

Этот проект представляет собой RESTful API для управления постами, комментариями и подписками. Пользователи могут создавать, читать, обновлять и удалять посты и комментарии. Также пользователи могут подписываться на других пользователей, чтобы получать уведомления о новых постах. Доступ к определенным действиям ограничен правами авторов.

▎Технологии

• Django

• Django REST Framework

• PostgreSQL (или другая база данных)

▎Установка и развертывание

1. Клонируйте репозиторий:
   
   git clone git@github.com:ArtemAl-34/api_yatube.git
   
2. Создайте виртуальное окружение:
   
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте venvScriptsactivate
   
3. Установите зависимости:
   
   pip install -r requirements.txt
   
4. Настройте базу данных: Отредактируйте файл settings.py, чтобы указать настройки вашей базы данных.

5. Примените миграции:
   
   python3 manage.py migrate
   
6. Запустите сервер:
   
   python3 manage.py runserver
      Теперь ваше API доступно по адресу http://127.0.0.1:8000/.

▎Информация об авторе

Имя автора: Альсимов Артем  
Контактная информация: arfey163@mail.ru  
GitHub: https://github.com/ArtemAl-34

▎Примеры запросов и ответов

▎Получить список групп

Запрос:
GET /api/groups/
Ответ:
[
    { "id": 1, "name": "Группа 1" },
    { "id": 2, "name": "Группа 2" }
]
▎Создать пост

Запрос:
POST /api/posts/
Content-Type: application/json
Authorization: Token ваш_токен

{
    "title": "Заголовок поста",
    "content": "Содержимое поста",
    "group": 1
}
Ответ:
{
    "id": 1,
    "title": "Заголовок поста",
    "content": "Содержимое поста",
    "author": 1,
    "group": 1,
    "created_at": "2023-01-01T12:00:00Z"
}
▎Добавить комментарий к посту

Запрос:
POST /api/posts/1/comments/
Content-Type: application/json
Authorization: Token ваш_токен

{
    "text": "Это комментарий"
}
Ответ:
{
    "id": 1,
    "text": "Это комментарий",
    "author": 1,
    "post": 1,
    "created_at": "2023-01-01T12:00:00Z"
}
▎Подписаться на пользователя

Запрос:
POST /api/users/1/subscribe/
Content-Type: application/json
Authorization: Token ваш_токен
Ответ:
{
    "message": "Вы успешно подписались на пользователя 1."
}
▎Отменить подписку на пользователя

Запрос:
DELETE /api/users/1/unsubscribe/
Content-Type: application/json
Authorization: Token ваш_токен
Ответ:
{
    "message": "Вы успешно отменили подписку на пользователя 1."
}
▎Получить список подписок пользователя

Запрос:
GET /api/users/me/subscriptions/
Authorization: Token ваш_токен
Ответ:
[
    { "id": 1, "username": "user1" },
    { "id": 2, "username": "user2" }
]
