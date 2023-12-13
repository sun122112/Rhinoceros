"""Tests of the delete task view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, User


class DeleteTaskViewTestCase(TestCase):
    """Tests of the delete task view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/tasks.json',
        'tasks/tests/fixtures/task_with_team.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.task_without_team = Task.objects.get(pk=1)
        self.task_with_team = Task.objects.get(pk=2)
        self.url_without_team = reverse('delete_task', kwargs={'task_id': self.task_without_team.id})
        self.url_with_team = reverse('delete_task', kwargs={'task_id': self.task_with_team.id})

    def test_delete_task_without_team_url(self):
        expected_url = f'/dashboard/delete_task/{self.task_without_team.id}/'
        self.assertEqual(self.url_without_team, expected_url)

    def test_delete_task_with_team_url(self):
        expected_url = f'/dashboard/delete_task/{self.task_with_team.id}/'
        self.assertEqual(self.url_with_team, expected_url)

    def test_get_delete_task_without_team(self):
        response = self.client.get(self.url_without_team)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_task.html')
        task = response.context['task']
        self.assertEqual(task, self.task_without_team)

    def test_get_delete_task_with_team(self):
        response = self.client.get(self.url_with_team)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_task.html')
        task = response.context['task']
        self.assertEqual(task, self.task_with_team)

    def test_successful_delete_task_without_team(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url_without_team, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('my_tasks')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_tasks.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Task Deleted!")

    def test_successful_delete_task_with_team(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url_with_team, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('team_info', kwargs={'team_id': self.task_with_team.team_id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'team_info.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Team Task Deleted!")

    def test_delete_task_has_team(self):
        self.assertIsNotNone(self.task_with_team.team)

