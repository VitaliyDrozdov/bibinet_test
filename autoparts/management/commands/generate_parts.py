import random
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from autoparts.models import Mark, Model, Part

PART_NAMES = [
    "Бампер передний",
    "Фара левая",
    "Дверь задняя",
    "Капот",
    "Решетка радиатора",
]
JSON_KEYS = ["color", "is_new_part", "count"]
COLORS = [
    "черный",
    "белый",
    "красный",
    "синий",
    "зеленый",
    "серый",
    "желтый",
    "оранжевый",
    "фиолетовый",
]


class Command(BaseCommand):
    help = "Создание запчастей для БД."

    def handle(self, *args: Any, **options: Any) -> str | None:
        marks = Mark.objects.all()
        models = Model.objects.all()
        with transaction.atomic():
            for _ in range(10000):
                mark = random.choice(marks)
                model = random.choice(models)
                name = random.choice(PART_NAMES)
                price = random.uniform(100, 10000)
                json_data = {
                    "color": random.choice(COLORS),
                    "is_new_part": random.choice([True, False]),
                    "count": random.randint(1, 20),
                }
                is_new_part = random.choice([True, False])
                part = Part.objects.create(
                    mark=mark,
                    model=model,
                    name=name,
                    price=price,
                    json_data=json_data,
                    is_visible=True,
                    is_new_part=is_new_part,
                )
                part.save()
        self.stdout.write("Запчасти созданы.")
