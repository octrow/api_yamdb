import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    current_year = datetime.datetime.now().year
    if (
        value < -32768 or value > current_year
    ):  # А чем не устроили произведения Древней Греции и Рима?
        raise ValidationError(
            f"{value} не подходит для года, попробуйте еще раз"
        )
