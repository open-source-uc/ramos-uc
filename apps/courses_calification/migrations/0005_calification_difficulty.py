# Generated by Django 3.2.5 on 2022-01-01 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses_calification", "0004_auto_20211230_1803"),
    ]

    operations = [
        migrations.AddField(
            model_name="calification",
            name="difficulty",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
