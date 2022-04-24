# Generated by Django 3.2.5 on 2021-12-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses_calification", "0003_auto_20210722_2131"),
    ]

    operations = [
        migrations.AddField(
            model_name="calification",
            name="comment",
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name="calification",
            name="credits",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]