# Generated by Django 5.0.3 on 2025-01-13 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("univeristy", "0014_delete_imageprompt_university_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventPlayerRegister",
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
                ("full_name", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField()),
                ("age", models.PositiveIntegerField()),
                ("phone_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=128)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Confirmed", "Confirmed"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                ("request_date", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="univeristy.event",
                    ),
                ),
                (
                    "university",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="univeristy.university",
                    ),
                ),
            ],
        ),
    ]
