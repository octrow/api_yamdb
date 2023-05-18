import re

from rest_framework.serializers import ValidationError


def username_valid(value):
    """
    Нельзя использовать имя пользователя 'me'.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    prohibited_usernames = ("me",)
    if value in prohibited_usernames:
        raise ValidationError("Недопустимое имя пользователя")
    pattern = r"^[\w.@+-]+\Z"  # Это константа, ей место в файле для констант.
    if not re.search(pattern, value):
        raise ValidationError("Только буквы, цифры и символы @/./+/-/_ .")  #
        # Какой конкретно символ я ввел не тот? Я - простой пользователь не
        # знаю, а разбираться в этих слешах минусах и плюсах, я не хочу,
        # загуглю другой сервис. Используем re.sub, чтобы найти всю запрещенку
        # и вывести её в исключении.
    return value
