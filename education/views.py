from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from education.models import Answer, Materials, Question, Section, Testing, UserTestProgress
from education.serializers import (AnswerSerializer, MaterialsSerializer, QuestionSerializer, SectionSerializer,
                                   TestingSerializer, UserTestProgressSerializer)
from users.permissions import IsAdmin, IsOwner


class SectionViewSet(ModelViewSet):
    """ViewSet для модели разделов"""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ("id", "title",)
    search_fields = ("title", "description",)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = (IsOwner | IsAdmin,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        return [permission() for permission in self.permission_classes]


class MaterialsViewSet(ModelViewSet):
    """ViewSet для модели материалов"""

    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ("id", "title", "section",)
    search_fields = ("title", "content", "section__title",)
    filterset_fields = ("section",)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = (IsOwner | IsAdmin,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        return [permission() for permission in self.permission_classes]


class TestingListCreateAPIView(ListCreateAPIView):
    """Generic-класс для создания и вывода списка тестов"""

    queryset = Testing.objects.all()
    serializer_class = TestingSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ("id", "title", "materials",)
    search_fields = ("title", "materials__title",)
    filterset_fields = ("materials",)


class QuestionListCreateAPIView(ListCreateAPIView):
    """Generic-класс для создания и вывода списка вопросов"""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ("id", "text", "test",)
    search_fields = ("text", "test__title",)
    filterset_fields = ("test",)


class AnswerListCreateCreateAPIView(ListCreateAPIView):
    """Generic-класс для создания и вывода списка ответов"""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserTestProgressView(RetrieveUpdateAPIView):
    """Generic-класс для прохождения тестов.
    Через метод GET получаем список вопросов по выбранной теме.
    С помощью метода PATCH отправляем ответ в виде {"answer_id": pk}.
    По завершении теста выводится статистика.
    Сбросить результаты и начать тест заново можно с помощью отправки POST запроса."""

    queryset = UserTestProgress.objects.all()
    serializer_class = UserTestProgressSerializer

    def get_object(self):
        """Получение списка вопросов из модели тестирования"""

        test = get_object_or_404(Testing, id=self.kwargs['pk'])
        progress, created = UserTestProgress.objects.get_or_create(user=self.request.user, test=test)
        return progress

    def get(self, request, *args, **kwargs):
        """Метод для получения первого вопроса из списка, либо вывод статистики, если тест уже завершился"""

        instance = self.get_object()
        if instance.current_question is None and not instance.is_complete:
            # Устанавливаем первый вопрос при первом запросе
            next_question = instance.test.question_set.order_by('id').first()
            if next_question:
                instance.current_question = next_question
                instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Метод для отправки ответов на вопрос"""

        instance = self.get_object()
        if instance.is_complete:
            return Response({"detail": "Тест уже завершен. (Можно выполнить сброс статистики и начать заново.)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Получаем текущий вопрос
        current_question = instance.current_question
        if current_question is None:
            return Response({"detail": "Нет текущего вопроса."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем ответ пользователя
        answer_id = request.data.get('answer_id')
        if not answer_id:
            return Response({"detail": "Ответ не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            answer = Answer.objects.get(id=answer_id, question=current_question)
        except Answer.DoesNotExist:
            return Response({"detail": "Нет ответа с таким id. (Выполните GET запрос для повторной попытки)"},
                            status=status.HTTP_400_BAD_REQUEST)

        if answer.is_correct:
            instance.correct_answers_count += 1

        # Получаем следующий вопрос
        next_question = instance.test.question_set.filter(id__gt=current_question.id).order_by('id').first()

        if next_question is None:
            instance.is_complete = True
            instance.current_question = None
            instance.save()
            return Response({"detail": "Тест завершен. (Можно выполнить сброс статистики и начать заново.)",
                             "correct_answers_count": instance.correct_answers_count},
                            status=status.HTTP_200_OK)

        # Обновляем текущий вопрос
        instance.current_question = next_question
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, pk=None):
        """Метод для сброса статистики ответов на вопросы"""

        instance = self.get_object()

        instance.current_question = None
        instance.is_complete = False
        instance.correct_answers_count = 0
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
