# Generated by Django 5.0.7 on 2024-07-16 04:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="owner",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Владелец"),
        ),
    ]
