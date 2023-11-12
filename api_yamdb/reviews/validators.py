from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


username_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    'Поле username не соответствует формату.'
)


def validate_year(value):
    """Валидация проверки года в модели Title."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год не может быть больше текущего года.',
            params={'value': value},
        )


def validate_username_me(value):
    """Проверяет username на использование значения "me"."""
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )
    return value
