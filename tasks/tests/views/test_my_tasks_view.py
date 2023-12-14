"""Tests of the my tasks view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Task

class MyTasksViewTestCase(TestCase):
    """Tests of the my tasks view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('my_tasks')
        self.user = User.objects.get(username='@johndoe')

    def test_my_tasks_url(self):
        self.assertEqual(self.url,'/dashboard/my_tasks/')

    def test_get_my_tasks(self):
        self.client.login(username=self.user.username, password="Password123")        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_tasks.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/log_in/?next=' + self.url)

    