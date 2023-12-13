"""Tests of the edit task view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, User


class EditTaskViewTestCase(TestCase):
    """Tests of the edit task view."""

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
        self.url_without_team = reverse('edit_task', kwargs={'task_id': self.task_without_team.id})
        self.url_with_team = reverse('edit_task', kwargs={'task_id': self.task_with_team.id})

    def test_edit_task_without_team_url(self):
        expected_url = f'/dashboard/my_tasks/edit_task/{self.task_without_team.id}/'
        self.assertEqual(self.url_without_team, expected_url)

    def test_edit_task_with_team_url(self):
        expected_url = f'/dashboard/my_tasks/edit_task/{self.task_with_team.id}/'
        self.assertEqual(self.url_with_team, expected_url)

    def test_get_edit_task_without_team(self):
        response = self.client.get(self.url_without_team)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_task.html')
        task = response.context['task']
        self.assertEqual(task, self.task_without_team)

    def test_get_edit_task_with_team(self):
        response = self.client.get(self.url_with_team)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_task.html')
        task = response.context['task']
        self.assertEqual(task, self.task_with_team)

    def test_successful_edit_task_without_team(self):
        form_input = {
            'task_name': 'Edited test task',
            'task_description': 'This is an edited test task.',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'done',
        }
        response = self.client.post(self.url_without_team, data=form_input, follow=True)
        response_url = reverse('my_tasks')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_tasks.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Task Details Updated!")
        response = self.client.post(self.url_without_team, data=form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        edited_task = Task.objects.get(id=self.task_without_team.id)
        self.assertIsNone(edited_task.team)


    def test_successful_edit_task_with_team(self):
        form_input = {
            'task_name': 'Update Team task',
            'task_description': 'This is a update for team task.',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'done',
        }
        response = self.client.post(self.url_with_team, data=form_input, follow=True)
        response_url = reverse('team_info', kwargs={'team_id': self.task_with_team.team_id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Team Task Details Updated!")

    def test_edit_task_without_assigned_user(self):
        form_input = {
            'task_name': 'Edited test task',
            'task_description': 'This is an edited test task.',
            'due': '2023-12-30',
            'status': 'done',
        }
        response = self.client.post(self.url_without_team, data=form_input, follow=True)
        response_url = reverse('my_tasks')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_tasks.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Task Details Updated!")
        edited_task = Task.objects.get(id=self.task_without_team.id)
        self.assertEqual(edited_task.assigned, self.user)