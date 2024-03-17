from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task
from projects.models import Project
from django.contrib.auth.models import User

class TaskAPITests(APITestCase):
    def setUp(self):
        self.project1 = Project.objects.create(title='Project 1', description='Description 1')
        self.project2 = Project.objects.create(title='Project 2', description='Description 2')
        
        self.user1 = User.objects.create(username='firstUser', password='1505@June')
        self.user2 = User.objects.create(username='secondUser', password='1505@June')
        self.user3 = User.objects.create(username='thirdUser', password='1505@June')

        self.task1 = Task.objects.create(
            project=self.project1,
            name='Task 1',
            description='Description 1',
            due_date='2024-03-16',
            status='todo',
        )
        self.task1.assigned_to.add(self.user1)

        self.task2 = Task.objects.create(
            project=self.project2,
            name='Task 2',
            description='Description 2',
            due_date='2024-03-17',
            status='in_progress',
        )
        self.task2.assigned_to.add(self.user1, self.user2)

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'project': self.project1.pk,
            'name': 'New Task',
            'description': 'New Description',
            'due_date': '2024-03-18',
            'status': 'done',
            'assigned_to':[self.user3.pk,self.user1.pk]

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        
        # Get the created task
        created_task = Task.objects.latest('created_at')
        
        # Get the sorted list of assigned user primary keys
        assigned_users = sorted(created_task.assigned_to.values_list('pk', flat=True))
        expected_users = sorted([self.user3.pk, self.user1.pk])
        
        # Assert that the assigned users are correct
        self.assertEqual(assigned_users, expected_users)

    def test_get_task_detail(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Task 1')

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        data = {
            'project': self.task1.project.pk,  # Access project primary key directly
            'name': 'Updated Task',
            'description': 'Updated Description',
            'due_date': '2024-03-20',
            'status': 'done',
            'assigned_to': [self.user3.pk,self.user1.pk, self.user2.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task')

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
