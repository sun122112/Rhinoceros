"""Tests of the task view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, User


class CreateTaskViewTestCase(TestCase):
    """Tests of the create task view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('task') 
        self.form_input = {
            'task_name': 'Test task',
            'content': 'Test create task function',
            'due': '2024-11-27 19:00:00',
        }
        self.user = User.objects.get(username='@johndoe')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/dashboard/task/')

    def test_successful_create_task(self):
        self.client.login(username=self.user.username, password='Password123')

        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)

        task_created = Task.objects.last()
        self.assertEqual(task_created.task_name, self.form_input['task_name'])
        self.assertEqual(task_created.content, self.form_input['content'])
        self.assertEqual(task_created.due.strftime('%Y-%m-%d %H:%M:%S'), self.form_input['due'])

        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
