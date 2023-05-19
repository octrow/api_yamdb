import datetime

from django.core.exceptions import ValidationError
from api_yamdb import constances


def year_validator(value):
    current_year = datetime.datetime.now().year
    if value < constances.MINYEAR or value > constances.CURRENTYEAR:
        raise ValidationError(
            f"{value} не подходит для года, попробуйте еще раз"
        )
