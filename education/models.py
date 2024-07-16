from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Section(models.Model):
    """Модель разделов обучения"""

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ("id",)


class Materials(models.Model):
    """Модель материалов для обучения"""

    title = models.CharField(max_length=150, verbose_name="Название")
    content = models.TextField(**NULLABLE, verbose_name="Содержание")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, **NULLABLE, verbose_name="Раздел обучения")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор")

    def __str__(self):
        return f"{self.section} - {self.title}"

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ("id",)


class Testing(models.Model):
    """Модель тестирования студентов"""

    title = models.CharField(max_length=100, verbose_name="Название")
    materials = models.ForeignKey(Materials, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Материалы для теста",
                                  related_name="testing_materials")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    correct_answers = models.IntegerField(default=0, verbose_name="Правильные ответы")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ("id",)


class Question(models.Model):
    """Модель вопросов тестирования"""

    text = models.TextField(verbose_name="Текст вопроса")
    test = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name="Тест")

    def __str__(self):
        return f"{self.test}: {self.text}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    """Модель ответов на вопросы по тестированию"""

    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return f"{self.question}: {self.text} - {self.is_correct}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserTestProgress(models.Model):
    """Модель прохождения пользователем тестирования"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    test = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name="Тест")
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, **NULLABLE,
                                         verbose_name="Текущий вопрос")
    is_complete = models.BooleanField(default=False, verbose_name="Завершено")
    correct_answers_count = models.IntegerField(default=0, verbose_name="Количество правильных ответов")

    def __str__(self):
        return f"{self.user} - {self.test} - {self.current_question}"

    class Meta:
        unique_together = ("user", "test")
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогрессы пользователей"
