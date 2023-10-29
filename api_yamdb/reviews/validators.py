import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy


symbol_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Латинский алфавит, цифры, подчеркивание. '
)


def validate_year(value):
    """
    Валидация проверки года в модели Title.
    """

    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            gettext_lazy('Год не может быть больше текущего года.'),
            params={'value': value},
        )