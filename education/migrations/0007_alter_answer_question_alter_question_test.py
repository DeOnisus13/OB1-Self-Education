# Generated by Django 5.0.7 on 2024-07-16 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0006_testing_correct_answers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="education.question", verbose_name="Вопрос"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="education.testing", verbose_name="Тест"
            ),
        ),
    ]
