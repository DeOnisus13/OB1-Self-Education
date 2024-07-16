from django.contrib import admin

from education.models import Answer, Materials, Question, Section, Testing


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """"""
    list_display = ("id", "title",)


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "section", "owner",)
    search_fields = ("title", "section__title",)


@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "materials",)
    list_filter = ("materials",)
    search_fields = ("title", "materials__title", "description",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "test",)
    list_filter = ("test",)
    search_fields = ("text", "test__title",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "question", "is_correct",)
    list_filter = ("question",)
    search_fields = ("text", "question__text",)
