## Описание ✒
REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. (Коллективный проект 3 студентов Яндекс.Практикум)

## Cтек ⚙️
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![Simple JWT](https://img.shields.io/badge/-SimpleJWT-464646?style=flat&color=008080)](https://jwt.io/)
[![SQLite]((https://img.shields.io/badge/-SQLite-464646?style=flat&color=008080))](https://www.sqlite.org/)

### Запуск проекта ▶
1. Клонирование репозитория
```
https://github.com/octrow/api_yamdb.git
```
2. Переходим в папку репозитория и создаём виртуальное окружение
```
cd api_yamdb
linux: python3 -m venv venv
windows: python -m venv venv
```
3. Активируем виртуальное окружение
```
windows: source venv/Scripts/activate
linux: source venv/bin/activate
```
4. Устанавливаем зависимости
```
windows: python -r requirements.txt
linux: python3 -r requirements.txt
5. Выполнение миграций
```
windows: python manage.py migrate
linux: python3 manage.py migrate
```
6. Запуск проекта
```
windows: python manage.py runserver
linux: python3 manage.py runserver
```

## Ссылки
### Документация API YaMDb - эндпойнт:
```json
/redoc/
```
http://localhost:8000/redoc/
### Развёрнутый проект:
http://localhost:8000/api/v1/  
http://localhost:8000/admin/

## Авторы
[Dmitry1Kovalev](https://github.com/Dmitry1Kovalev)  
[Sukhov11](https://github.com/Sukhov11)  
[octrow](https://github.com/octrow)  
Проект разрабатывался в команде, ссылка на репозиторий:  
https://github.com/octrow/api_yamdb