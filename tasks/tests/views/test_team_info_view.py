"""Unit tests of the team info view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, Team, User

class TeamInfoViewTestCase(TestCase):
    """Unit tests of the team info view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json',
        'tasks/tests/fixtures/tasks.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.team = Team.objects.get(id=1)
        self.url = reverse('team_info', kwargs={'team_id': self.team.id})

    def test_team_info_url(self):
        self.assertEqual(self.url, f'/dashboard/my_teams/team_info/{self.team.id}/')

    def test_get_team_info(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team_info.html')
        team = response.context['team']
        self.assertEqual(team, self.team)

    def test_team_info_contains_tasks(self):
        response = self.client.get(self.url)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), Task.objects.filter(team=self.team).count())