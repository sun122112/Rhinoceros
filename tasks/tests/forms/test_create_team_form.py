"""Tests of the task view."""
from django import forms
from django.test import TestCase
from tasks.forms import CreateTeamForm
from tasks.models import User, Team

class CreateTeamFormTestCase(TestCase):
    """Unit tests of the form for creating teams."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.form_input = {
            'team_name': 'Test Team B', 
            'team_description': 'Another test team'
        }

    def test_form_contains_required_fields(self):
        form = CreateTeamForm()
        self.assertIn('team_name',form.fields)
        self.assertIn('team_description',form.fields)

    def test_valid_create_teams_form(self):
        form = CreateTeamForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_rejects_blank_team_name(self):
        self.form_input['team_name'] = ''
        form = CreateTeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_rejects_blank_team_description(self):
        self.form_input['team_description'] = ''
        form = CreateTeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_created_team_must_save_correctly(self):
        form = CreateTeamForm(data=self.form_input)
        before_count=Team.objects.count()
        form.save()
        after_count=Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        team=Team.objects.get(id=1)
        self.assertEqual(team.team_name, 'Test Team B')
        self.assertEqual(team.team_description, 'Another test team')

    def test_form_does_not_save_when_commit_is_false(self):
        form = CreateTeamForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        team = form.save(commit=False)
        self.assertIsNone(team.id)