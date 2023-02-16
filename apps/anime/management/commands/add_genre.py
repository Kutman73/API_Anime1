from django.core.management import BaseCommand
from apps.anime.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        genres_tuple = (
            'Приключения', 'Боевик', 'Комедия', 'Повседневность',
            'Романтика', 'Драма', 'Фантастика', 'Фэнтези',
            'Мистика', 'Детектив', 'Триллер', 'Психология'
        )
        Genre.objects.all().delete()
        for i in genres_tuple:
            Genre.objects.create(genre_name=i)
        print("Added genres status: OK")
