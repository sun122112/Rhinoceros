"""Unit tests for the Team model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Team

class TeamModelTestCase(TestCase):
    """Unit tests for the Team model."""


    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(id = 1)

    def test_valid_team(self):
        self._assert_team_is_valid()

    def test_team_name_can_be_50_characters_long(self):
        self.team.team_name = 'x' * 50
        self._assert_team_is_valid()

    def test_team_name_cannot_be_over_50_characters_long(self):
        self.team.team_name = 'x' * 51
        self._assert_team_is_invalid()
    
    def test_team_description_can_be_200_characters_long(self):
        self.team.team_description = 'x' * 200
        self._assert_team_is_valid()

    def test_team_description_cannot_be_over_200_characters_long(self):
        self.team.team_description = 'x' * 201
        self._assert_team_is_invalid()

    def test_team_members_can_be_added(self):
        self.team.team_members.add(User.objects.get(username='@janedoe'))
        self._assert_team_is_valid()

    def test_team_members_can_be_removed(self):
        self.team.team_members.remove(User.objects.get(username='@johndoe'))
        self._assert_team_is_valid()
    





    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except (ValidationError):
            self.fail('Test team should be valid')

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()