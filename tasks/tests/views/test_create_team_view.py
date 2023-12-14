"""Unit tests of the create team view."""
from django.test import TestCase
from django.urls import reverse
from tasks.forms import CreateTeamForm
from tasks.models import User, Team

class CreateTeamViewTest(TestCase):
    """Unit tests of the create team view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_team')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.form_input = {
            'team_name': 'Test Team B', 
            'team_description': 'Another test team'
        }

    def test_create_team_url(self):
        self.assertEqual(self.url,'/dashboard/create_team/')

    def test_get_create_team(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_create_team(self):
        self.form_input['team_name'] = ''
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertTrue(form.is_bound)


    def test_succesful_create_team(self):
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('my_teams')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_teams.html')
        team = Team.objects.last()
        self.assertIsNotNone(team)
        self.assertEqual(team.team_name, self.form_input['team_name'])
        self.assertEqual(team.team_description, self.form_input['team_description'])