"""Unit tests of the edit team view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import Team, User


class EditTeamViewTestCase(TestCase):
    """Unit tests of the edit team view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.team = Team.objects.get(id=1)
        self.url= reverse('edit_team', kwargs={'team_id': self.team.id})

    def test_edit_team_url(self):
        self.assertEqual(self.url, f'/dashboard/my_teams/edit_team/{self.team.id}/')
        
    def test_get_edit_team(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_team.html')
        team = response.context['team']
        self.assertEqual(team, self.team)

    def test_successful_edit_team_details_updated(self):
        """Form submitted with valid data, Team details updated, User redirected correctly, Message works correctly."""
        form_input = {
            'team_name': 'Edited Team Name',
            'team_description': 'Edited Team Description'

        }
        response = self.client.post(self.url, data=form_input, follow=True)
        response_url = reverse('my_teams')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Team Details Updated!")
    
    def test_unsuccessful_edit_team_from_invalid_team_name(self):
        form_input = {
            'team_name': '', 
            'team_description': 'Edited Team Description'
        }
        response = self.client.post(self.url, data=form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_unsuccessful_edit_team_from_invalid_team_description(self):
        form_input = {
            'team_name': 'Edit Team Name', 
            'team_description': ''
        }
        response = self.client.post(self.url, data=form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    