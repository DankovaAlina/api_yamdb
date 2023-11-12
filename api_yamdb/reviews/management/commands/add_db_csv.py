import csv
from django.apps import apps
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


TitleGenre = apps.get_model('reviews', 'title_genre')

DATA_SOURCES_FOR_MOVIE_DATABASE = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    User: 'static/data/users.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    TitleGenre: 'static/data/genre_title.csv',
}


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из CSV-файлов'

    def handle(self, *args, **options):
        for key, value in DATA_SOURCES_FOR_MOVIE_DATABASE.items():
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
                    model.objects.get_or_create(**row)

            self.stdout.write(self.style.SUCCESS(
                f'Данные из {csv_file} успешно загружены в базу данных'
            ))

        self.stdout.write(self.style.SUCCESS(
            'Все данные успешно загружены в базу данных!'
        ))
