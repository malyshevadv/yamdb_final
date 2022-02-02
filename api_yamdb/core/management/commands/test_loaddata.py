import csv
import os

from core.serializers import (CategoryLoadSerializer, CommentLoadSerializer,
                              GenreLoadSerializer, ReviewLoadSerializer,
                              TitleGenresLoadSerializer, TitleLoadSerializer,
                              UserLoadSerializer)
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load data from csv to db'

    DATA_SERIALIZERS = {
        'category.csv': (CategoryLoadSerializer, 'category'),
        'comments.csv': (CommentLoadSerializer, 'comment'),
        'genre.csv': (GenreLoadSerializer, 'genre'),
        'genre_title.csv': (TitleGenresLoadSerializer, 'genre_title'),
        'review.csv': (ReviewLoadSerializer, 'review'),
        'titles.csv': (TitleLoadSerializer, 'title'),
        'users.csv': (UserLoadSerializer, 'user'),
    }

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        file_names = options['file_name']

        for name in file_names:
            path = os.path.join(settings.BASE_DIR, 'static/data/', name)

            with open(path, encoding='utf-8', newline='') as csvfile:
                data = csv.DictReader(csvfile)

                for each in data:
                    serializer_class, data_name = (
                        self.DATA_SERIALIZERS[name]
                    )
                    serializer = serializer_class(data=each)

                    if serializer.is_valid():
                        serializer.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Successfully added {} {}'.format(
                                    data_name,
                                    serializer.data
                                )
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                'An error occurred while loading {}:{}'.format(
                                    data_name,
                                    serializer.errors
                                )
                            )
                        )
