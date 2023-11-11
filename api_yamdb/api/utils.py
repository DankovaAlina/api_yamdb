from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.consts import ADMIN_EMAIL


def send_confirmation_code(user):
    """Отправляет код подтверждения пользователю."""
    send_mail(
        subject='Подтверждение регистрации',
        message=f'Код подтверждения - {generate_confirmation_code(user)}',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def generate_confirmation_code(user):
    """Генерирует код подтверждения при регистрации пользователя."""
    return default_token_generator.make_token(user)


def check_confirmation_code(user, confirmation_code):
    """Проверяет код подтверждения."""
    return default_token_generator.check_token(user, confirmation_code)
