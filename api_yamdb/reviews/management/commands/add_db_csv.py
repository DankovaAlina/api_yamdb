import csv
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)


MY_DICT = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    User: 'static/data/users.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    # TitleGenre: 'static/data/genre_title.csv',
}

# словарь для добавления связей many to many
# key - основная модель
# value - зависимая модель, название поля связи, csv файл
MTM_DICT = {
    Title: (Genre, 'genre', 'static/data/genre_title.csv')
}


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из CSV-файлов'

    def handle(self, *args, **options):
        for key, value in MY_DICT.items():
            csv_file = value

            # Получаем модель
            try:
                model = key
            except NameError:
                self.stdout.write(self.style.ERROR('Модель не найдена'))
                return

            # Заполняем модель данными из CSV-файла
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS(
                f'Данные из {csv_file} успешно загружены в базу данных'
            ))

# цикл по обработке словаря many to many
        for key, value in MTM_DICT.items():
            related_model = value[0]
            related_field = value[1]
            csv_file = value[2]

            parent_model = key

            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title_obj = parent_model.objects.filter(id=row[1]).first() # получаем объект основной модели по id из csv
                    genre_obj = related_model.objects.filter(id=row[2]).first() # получаем объект зависимой модели по id из csv

                    # getattr(title_obj, related_field) - первый аргумент это объект оснвной модели, второй - название поля связи M2M у основной модели
                    # .add(genre_obj) - добавление зависимого объекта в поле связи M2M у основной модели

                    getattr(title_obj, related_field).add(genre_obj)

        self.stdout.write(self.style.SUCCESS(
            'Все данные успешно загружены в базу данных!'
        ))
