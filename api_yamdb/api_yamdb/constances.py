import datetime


DEFAULT_FROM_EMAIL = "kov.dima.seaman@mail.ru"
SUBJECT = "Регистрация на сайте"
EMAIL_TAKEN_ERROR = "Электронная почта уже занята!"
USERNAME_TAKEN_ERROR = "Имя пользователя уже занято!"
MESSAGE_EMAIL = "Здравствуйте, {}.\nКод подтверждения для доступа: ."

LENGTH_NAME = 150
LENGTH_EMAIL = 254
LENGTH_SLUG = 50
LENGTH_REALNAME = 256

MINYEAR = -32768
CURRENTYEAR = datetime.datetime.now().year

PATTERN = r"^[\w.@+-]+\Z"
