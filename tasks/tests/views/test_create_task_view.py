"""Tests of the task view."""
from django.test import TestCase
from django.urls import reverse

from tasks.forms import CreateTaskForm
from tasks.models import Task, User


class CreateTaskViewTestCase(TestCase):
    """Tests of the create task view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_task')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.form_input = {
            'task_name': 'Test task',
            'task_description': 'This is a test task.',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'not_started',
        }

    def test_create_task_url(self):
        self.assertEqual(self.url, '/dashboard/create_task/')

    def test_get_create_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertFalse(form.is_bound)

    def test_successful_create_task(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('my_tasks')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_tasks.html')

    def test_unsuccessful_create_task(self):
        self.form_input['task_name'] = ''
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertTrue(form.is_bound)
