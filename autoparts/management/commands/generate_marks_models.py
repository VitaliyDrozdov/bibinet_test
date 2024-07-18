from django.core.management.base import BaseCommand

from autoparts.models import Mark, Model

MARKS = [
    {"name": "Toyota", "producer_country_name": "Japan"},
    {"name": "Ford", "producer_country_name": "USA"},
    {"name": "BMW", "producer_country_name": "Germany"},
    {"name": "Hyundai", "producer_country_name": "South Korea"},
    {"name": "Renault", "producer_country_name": "France"},
]

MODELS = [
    {"name": "Corolla", "mark": "Toyota"},
    {"name": "Mustang", "mark": "Ford"},
    {"name": "X5", "mark": "BMW"},
    {"name": "Elantra", "mark": "Hyundai"},
    {"name": "Clio", "mark": "Renault"},
]


class Command(BaseCommand):
    help = "Создание моделей и марок."

    def handle(self, *args, **kwargs):
        for mark_data in MARKS:
            mark, created = Mark.objects.get_or_create(
                name=mark_data["name"],
                defaults={
                    "producer_country_name": mark_data[
                        "producer_country_name"
                    ],
                    "is_visible": True,
                },
            )
            if created:
                self.stdout.write(f"Марка создана: {mark.name}")

        for model_data in MODELS:
            mark = Mark.objects.get(name=model_data["mark"])
            model, created = Model.objects.get_or_create(
                name=model_data["name"],
                defaults={
                    "mark": mark,
                    "is_visible": True,
                },
            )
            if created:
                self.stdout.write(f"Модель создана: {model.name}")
