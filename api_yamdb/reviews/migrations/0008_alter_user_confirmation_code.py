# Generated by Django 3.2 on 2023-11-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='568678', max_length=6, verbose_name='Код подтверждения'),
        ),
    ]
