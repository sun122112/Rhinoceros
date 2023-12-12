"""Tests of the task view."""
from django import forms
from django.test import TestCase
from tasks.forms import CreateTeamForm
from tasks.models import User, Team

class CreateTeamFormTestCase(TestCase):
    """Unit tests of the form for creating teams."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.form_input = {'team_name': 'Team A', 'team_description': 'A team with 1 group member only.'}

    def test_form_contains_required_fields(self):
        form = CreateTeamForm()
        self.assertIn('team_name',form.fields)
        self.assertIn('team_description',form.fields)

    def test_form_accepts_valid_input(self):
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

    


    