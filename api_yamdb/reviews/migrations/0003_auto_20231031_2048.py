# Generated by Django 3.2 on 2023-10-31 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='descriptions',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='203186', max_length=6, verbose_name='Код подтверждения'),
        ),
    ]
