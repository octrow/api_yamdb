import re
from rest_framework.serializers import ValidationError


def username_valid(value):
    """
    Нельзя использовать имя пользователя 'me'.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    prohibited_usernames = ('me',)
    if value in prohibited_usernames:
        raise ValidationError('Недопустимое имя пользователя')
    pattern = r"^[\w.@+-]+\Z"
    if not re.search(pattern, value):
        raise ValidationError('Только буквы, цифры и символы @/./+/-/_ .')
    return value