"""Unit tests of the delete team view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Team, User


class DeleteTeamViewTestCase(TestCase):
    """Unit tests of the delete team view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.team = Team.objects.get(id=1)
        self.url= reverse('delete_team', kwargs={'team_id': self.team.id})

    def test_delete_team_url(self):
        self.assertEqual(self.url, f'/dashboard/delete_team/{self.team.id}/')
        
    def test_get_delete_team(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_team.html')
        team = response.context['team']
        self.assertEqual(team, self.team)

    def test_successful_delete_team(self):
        before_count = Team.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('my_teams')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_teams.html')
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Team Deleted!")

    