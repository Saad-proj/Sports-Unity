# Generated by Django 5.0.3 on 2025-01-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("univeristy", "0013_imageprompt"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ImagePrompt",
        ),
        migrations.AddField(
            model_name="university",
            name="password",
            field=models.CharField(default="default_password", max_length=128),
        ),
    ]
