"""Tests of the my teams view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User, Team

class MyTeamsViewTestCase(TestCase):
    """Tests of the my teams view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('my_teams')
        self.user = User.objects.get(username='@johndoe')

    def test_my_teams_url(self):
        self.assertEqual(self.url,'/dashboard/my_teams/')

    def test_get_my_teams(self):
        self.client.login(username=self.user.username, password="Password123")        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_teams.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/log_in/?next=' + self.url)