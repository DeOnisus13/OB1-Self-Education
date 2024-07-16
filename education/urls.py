from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import (AnswerListCreateCreateAPIView, MaterialsViewSet, QuestionListCreateAPIView,
                             SectionViewSet, TestingListCreateAPIView, UserTestProgressView)

app_name = EducationConfig.name

section_router = DefaultRouter()
section_router.register(r"section", SectionViewSet, basename="section")

materials_router = DefaultRouter()
materials_router.register(r"materials", MaterialsViewSet, basename="materials")

urlpatterns = [
    path("testing/", TestingListCreateAPIView.as_view(), name="testing"),
    path("question/", QuestionListCreateAPIView.as_view(), name="question"),
    path("answer/", AnswerListCreateCreateAPIView.as_view(), name="answer"),
    path("testing/<int:pk>/", UserTestProgressView.as_view(), name="user-test"),
    path("testing/<int:pk>/reset/", UserTestProgressView.as_view(), name="user-test-reset")
] + section_router.urls + materials_router.urls
