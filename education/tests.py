from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Answer, Materials, Question, Section, Testing
from users.models import User


class SectionTestCase(APITestCase):
    """Тесты для SectionViewSet"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.section = Section.objects.create(title="Section1", description="Description1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_section_retrieve(self):
        url = reverse("education:section-detail", args=(self.section.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.section.title)

    def test_section_create(self):
        url = reverse("education:section-list")
        data = {"title": "test_title"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.all().count(), 2)

    def test_section_update(self):
        url = reverse("education:section-detail", args=(self.section.pk,))
        data = {"title": "title_new"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "title_new")

    def test_section_delete(self):
        url = reverse("education:section-detail", args=(self.section.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.all().count(), 0)

    def test_section_list(self):
        url = reverse("education:section-list")
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'id': self.section.pk,
                       'materials_count': 0,
                       'materials': [],
                       'title': 'Section1',
                       'description': 'Description1',
                       'owner': self.user.pk}
                  ]
                  }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class MaterialsTestCase(APITestCase):
    """Тесты для MaterialsViewSet"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.materials = Materials.objects.create(title="Materials1", content="Description1", owner=self.user)
        self.section = Section.objects.create(title="Section1", description="Description1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_materials_retrieve(self):
        url = reverse("education:materials-detail", args=(self.materials.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.materials.title)

    def test_materials_create(self):
        url = reverse("education:materials-list")
        data = {"title": "test_title"}
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Materials.objects.all().count(), 2)

    def test_materials_update(self):
        url = reverse("education:materials-detail", args=(self.materials.pk,))
        data = {"title": "title_new"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "title_new")

    def test_materials_delete(self):
        url = reverse("education:materials-detail", args=(self.materials.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Materials.objects.all().count(), 0)

    def test_materials_list(self):
        url = reverse("education:materials-list")
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [
                      {'id': self.materials.pk,
                       'title': 'Materials1',
                       'content': 'Description1',
                       'section': None,
                       'owner': self.user.pk}
                  ]
                  }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class UserTestProgressViewTests(APITestCase):
    """Тест для UserTestProgressView"""

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.section = Section.objects.create(title='Section 1', description='Description 1', owner=self.user)
        self.material = Materials.objects.create(title='Material 1', content='Content 1', section=self.section,
                                                 owner=self.user)
        self.test = Testing.objects.create(title='Test 1', materials=self.material, description='Test Description')
        self.question1 = Question.objects.create(text='Question 1', test=self.test)
        self.answer1 = Answer.objects.create(text='Answer 1', question=self.question1, is_correct=True)
        self.answer2 = Answer.objects.create(text='Answer 2', question=self.question1, is_correct=False)
        self.question2 = Question.objects.create(text='Question 2', test=self.test)
        self.answer3 = Answer.objects.create(text='Answer 3', question=self.question2, is_correct=True)
        self.answer4 = Answer.objects.create(text='Answer 4', question=self.question2, is_correct=False)
        self.client.force_authenticate(user=self.user)

    def test_get_first_question(self):
        url = reverse('education:user-test', args=[self.test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_question', response.data)
        self.assertEqual(response.data['current_question']['text'], self.question1.text)

    def test_patch_answer_correct(self):
        url = reverse('education:user-test', args=[self.test.pk])
        self.client.get(url)
        response = self.client.patch(url, {'answer_id': self.answer1.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['correct_answers_count'], 1)

        if 'current_question' in response.data:
            self.assertEqual(response.data['current_question']['text'], self.question2.text)
        else:
            self.assertTrue(response.data['is_complete'])

    def test_patch_answer_incorrect(self):
        url = reverse('education:user-test', args=[self.test.pk])
        self.client.get(url)
        response = self.client.patch(url, {'answer_id': self.answer2.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_question', response.data)
        self.assertEqual(response.data['correct_answers_count'], 0)

    def test_complete_test(self):
        url = reverse('education:user-test', args=[self.test.pk])
        self.client.get(url)
        response = self.client.patch(url, {'answer_id': self.answer1.pk}, format='json')
        response = self.client.patch(url, {'answer_id': self.answer3.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get(url)
        self.assertTrue(self.client.get(url).data['is_complete'])
        self.assertEqual(response.data['correct_answers_count'], 2)

    def test_reset_test(self):
        url = reverse('education:user-test-reset', args=[self.test.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_complete'])
        self.assertEqual(response.data['correct_answers_count'], 0)
        self.assertIsNone(response.data['current_question'])
