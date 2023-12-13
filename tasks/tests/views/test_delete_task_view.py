"""Tests of the delete task view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, User


class DeleteTaskViewTestCase(TestCase):
    """Tests of the delete task view."""

    fixtures = ['tasks/tests/fixtures/default_user.json', 'tasks/tests/fixtures/tasks.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.task = Task.objects.get(pk=1)
        self.url = reverse('delete_task', kwargs={'task_id': self.task.id})

    def test_delete_task_url(self):
        expected_url = f'/dashboard/delete_task/{self.task.id}/'
        self.assertEqual(self.url, expected_url)

    def test_get_delete_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_task.html')
        task = response.context['task']
        self.assertEqual(task, self.task)

    def test_successful_delete_task(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('my_tasks')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_tasks.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Task Deleted!")

