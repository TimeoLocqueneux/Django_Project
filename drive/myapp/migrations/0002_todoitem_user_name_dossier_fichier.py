# Generated by Django 5.1.2 on 2024-10-30 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TodoItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("completed", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="Jean", max_length=255),
        ),
        migrations.CreateModel(
            name="Dossier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sous_dossiers",
                        to="myapp.dossier",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fichier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("file", models.FileField(upload_to="files/")),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fichiers",
                        to="myapp.dossier",
                    ),
                ),
            ],
        ),
    ]
