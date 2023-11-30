from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, User

class DeleteTaskViewTestCase(TestCase):
    """Tests of the delete task view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.task = Task.objects.create(
            task_name='Test task for deletion',
            content='Test delete task function',
            due='2024-11-27 19:00:00',
        )
        self.url = reverse('task')

    def test_successful_delete_task(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url, {'id': self.task.id}, follow=True)
        after_count = Task.objects.count()


        self.assertEqual(after_count, before_count - 1)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
