import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    current_year = datetime.datetime.now().year
    if value < 0 or value > current_year:
        raise ValidationError(
            f"{value} не подходит для года, попробуйте еще раз"
        )


def rating_validator(value):
    if value < 0 or value > 10:
        raise ValidationError(
            f"{value} не подходит для рейтинга, попробуйте еще раз"
        )
