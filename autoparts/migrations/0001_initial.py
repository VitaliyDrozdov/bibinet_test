# Generated by Django 3.1.12 on 2024-07-18 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mark",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Наименование"
                    ),
                ),
                (
                    "producer_country_name",
                    models.CharField(
                        db_index=True,
                        max_length=30,
                        verbose_name="Страна производитель",
                    ),
                ),
                ("is_visible", models.BooleanField(verbose_name="Видимость")),
            ],
        ),
        migrations.CreateModel(
            name="Model",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Наименование"
                    ),
                ),
                ("is_visible", models.BooleanField()),
                (
                    "mark",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="models",
                        to="autoparts.mark",
                        verbose_name="Модель",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=50,
                        verbose_name="Наименование запчасти",
                    ),
                ),
                ("price", models.FloatField(verbose_name="Цена")),
                ("json_data", models.JSONField()),
                ("is_visible", models.BooleanField(verbose_name="Видимость")),
                (
                    "is_new_part",
                    models.BooleanField(verbose_name="Новая запчасть"),
                ),
                (
                    "mark",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="autoparts.mark",
                        verbose_name="Марка",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="autoparts.model",
                        verbose_name="Модель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запчасть",
                "verbose_name_plural": "Запчасти",
                "ordering": ("name",),
            },
        ),
        migrations.AddIndex(
            model_name="part",
            index=models.Index(
                fields=["name", "is_visible"],
                name="autoparts_p_name_02978f_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="part",
            index=models.Index(
                fields=["mark", "is_visible"],
                name="autoparts_p_mark_id_d66710_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="part",
            index=models.Index(
                fields=["model", "is_visible"],
                name="autoparts_p_model_i_69ba81_idx",
            ),
        ),
    ]