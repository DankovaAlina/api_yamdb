import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy


symbol_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Латинский алфавит, цифры, подчеркивание. '
)


def validate_year(value):
    """Валидация проверки года в модели Title."""
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            gettext_lazy('Год не может быть больше текущего года.'),
            params={'value': value},
        )


username_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    'Поле username не соответствует формату.'
)


def validate_username_me(value):
    """Проверяет username на использование значения "me"."""
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )
    return value
