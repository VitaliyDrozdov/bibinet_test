from django.db import models


class Mark(models.Model):
    name = models.CharField("Наименование", max_length=50, unique=True)
    producer_country_name = models.CharField(
        "Страна производитель", max_length=30, db_index=True
    )
    is_visible = models.BooleanField("Видимость")

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField("Наименование", max_length=50, unique=True)
    mark = models.ForeignKey(
        Mark,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Модель",
        related_name="models",
    )
    is_visible = models.BooleanField()

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(
        "Наименование запчасти", max_length=50, db_index=True
    )
    mark = models.ForeignKey(
        Mark,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Марка",
        related_name="parts",
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Модель",
        related_name="parts",
    )
    price = models.FloatField("Цена")
    json_data = models.JSONField()
    is_visible = models.BooleanField("Видимость")
    is_new_part = models.BooleanField("Новая запчасть")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name", "is_visible"]),
            models.Index(fields=["mark", "is_visible"]),
            models.Index(fields=["model", "is_visible"]),
        ]
