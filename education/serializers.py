from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import SerializerMethodField

from education.models import Answer, Materials, Question, Section, Testing, UserTestProgress


class MaterialsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели материалов"""

    section = SlugRelatedField(slug_field="title", queryset=Section.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Materials
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели разделов"""

    materials_count = SerializerMethodField()
    materials = MaterialsSerializer(source="materials_set", many=True, read_only=True)

    def get_materials_count(self, obj):
        return obj.materials_set.all().count()

    class Meta:
        model = Section
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ответов на вопросы"""

    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели вопросов"""

    answers_count = SerializerMethodField()

    def get_answers_count(self, obj):
        return obj.answer_set.all().count()

    class Meta:
        model = Question
        fields = "__all__"


class TestingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тестирования пользователей"""

    questions_count = SerializerMethodField()
    questions = QuestionSerializer(source="question_set", many=True, read_only=True)

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

    class Meta:
        model = Testing
        fields = "__all__"


class AnswerQuizSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов пользователей при прохождении теста"""

    class Meta:
        model = Answer
        fields = ["id", "text"]


class QuestionQuizSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов при прохождении тестов"""

    answers = AnswerQuizSerializer(many=True, read_only=True, source="answer_set")

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]


class UserTestProgressSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода статистики при прохождении теста"""

    current_question = QuestionQuizSerializer(read_only=True)

    class Meta:
        model = UserTestProgress
        fields = ["id", "user", "test", "current_question", "is_complete", "correct_answers_count"]
