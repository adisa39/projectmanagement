# from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from .models import Project
from .views import ProjectViewSet

class ProjectAPITests(APITestCase):
    def setUp(self):
        self.project1 = Project.objects.create(title='Project 1', description='Description 1')
        self.project2 = Project.objects.create(title='Project 2', description='Description 2')
        self.factory = APIRequestFactory()
        self.view = ProjectViewSet.as_view({'get': 'list'})

    def test_get_projects(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_project(self):
        url = reverse('project-list')
        data = {'title': 'New Project', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)

    def test_get_single_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Project 1')

    def test_update_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project1.pk})
        data = {'title': 'Updated Project', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.title, 'Updated Project')

    def test_delete_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)

    def test_filter_by_status(self):
        url = reverse('project-list')
        request = self.factory.get(url, {'status': 'in_progress'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that only projects with status 'in_progress' are returned

    def test_search_by_title(self):
        url = reverse('project-list')
        request = self.factory.get(url, {'search': 'project'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that projects with titles containing 'project' are returned

    def test_search_by_description(self):
        url = reverse('project-list')
        request = self.factory.get(url, {'search': 'description'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that projects with descriptions containing 'description' are returned
    # More test cases for other API endpoints and functionalities
