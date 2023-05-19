from django.core.exceptions import ValidationError

from api_yamdb import constances


def year_validator(value):
    if value < constances.MINYEAR or value > constances.CURRENTYEAR:
        raise ValidationError(
            f"{value} не подходит для года, попробуйте еще раз"
        )
