import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from loguru import logger

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    help = "Импорт данных из файлов CSV."

    def handle(self, *args, **kwargs):
        name_models = {
            "category": Category,
            "genre": Genre,
            "titles": Title,
            "users": User,
            "review": Review,
            "comments": Comment,
            "genre_title": GenreTitle,
        }
        for name, model in name_models.items():
            file_path = os.path.join(
                settings.BASE_DIR, "static", "data", f"{name}.csv"
            )
            try:
                with open(file_path, encoding="utf-8") as data:
                    logger.info(f"Загрузка файла {name}.csv")
                    objects = []
                    for row in csv.DictReader(data):
                        fields = {}
                        for key, value in row.items():
                            if key == "category":
                                fields[key], _ = name_models[
                                    key
                                ].objects.get_or_create(id=value)
                            elif key == "author":
                                fields[key] = User.objects.get(id=value)
                            else:
                                fields[key] = value
                        objects.append(model(**fields))
                    model.objects.bulk_create(objects)
                    logger.info(f"Успешно загружен файл {name}.csv")
            except FileNotFoundError:
                logger.error(f"Файл {name}.csv не найден")
            except Exception as e:
                logger.error(f"Ошибка в процессе загрузки {name}.csv: {e}")
