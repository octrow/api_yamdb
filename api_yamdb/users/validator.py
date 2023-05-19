import re

from rest_framework.serializers import ValidationError

from api_yamdb import constances


def username_valid(value):
    """
    Нельзя использовать имя пользователя 'me'.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    prohibited_usernames = ("me",)
    if value in prohibited_usernames:
        raise ValidationError("Недопустимое имя пользователя")
    # pattern = r"^[\w.@+-]+\Z"
    # ГОТОВО! Это константа, ей место в файле для констант.
    if not re.search(constances.PATTERN, value):
        forbidden_chars = re.sub(constances.PATTERN, "", value)
        raise ValidationError(
            f"Только буквы, цифры и символы @/./+/-/_ ."
            f"Вы ввели: {forbidden_chars}"
        )
        # ГОТОВО! Какой конкретно символ я ввел не тот? Я - простой
        # пользователь не знаю, а разбираться в этих слешах минусах и плюсах,
        # я не хочу, загуглю другой сервис. Используем re.sub, чтобы найти всю
        # запрещенку и вывести её в исключении.
    return value
