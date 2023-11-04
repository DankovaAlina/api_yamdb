# Generated by Django 3.2 on 2023-11-03 22:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20231104_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10, message='Оценка не может быть выше 10'), django.core.validators.MinValueValidator(1, message='Оценка не может быть ниже 1')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='746977', max_length=6, verbose_name='Код подтверждения'),
        ),
    ]
