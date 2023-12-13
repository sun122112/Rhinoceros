"""Unit tests of the edit team form."""
from django import forms
from django.test import TestCase
from tasks.forms import EditTeamForm
from tasks.models import User, Team

class EditTeamFormTestCase(TestCase):
    """Tests of the edit team form."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json',
        ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.added_user = User.objects.create(username='@janedoe')
        self.team = Team.objects.get(id = 1)
        self.form_input = {
            'team_name': 'Edited Team Name',
            'team_description': 'Edited Team Description',
            'add_members': '@janedoe'
        }
        self.form = EditTeamForm(data=self.form_input, instance=self.team)


    def test_valid_edit_form(self):
        self.assertTrue(self.form.is_valid())

    def test_invalid_edit_form(self):
        form = EditTeamForm({}, instance=self.team)
        self.assertFalse(form.is_valid())

    def test_form_has_required_fields(self):
        form= EditTeamForm(instance=self.team)
        self.assertIn('team_name',form.fields)
        self.assertIn('team_description',form.fields)
        self.assertIn('add_members',form.fields)
        
    def test_form_rejects_edited_blank_team_name(self):
        self.form_input['team_name'] = ''
        self.assertFalse(self.form.is_valid())

    def test_form_rejects_edited_blank_team_description(self):
        self.form_input['team_description'] = ''
        self.assertFalse(self.form.is_valid())

    def test_form_saves_valid_team_correctly(self):
        self.assertTrue(self.form.is_valid())
        edited_team = self.form.save()
        self.assertEqual(edited_team.team_name, self.form_input['team_name'])
        self.assertEqual(edited_team.team_description, self.form_input['team_description'])
        self.assertIn(self.added_user, edited_team.team_members.all())

    def test_form_does_not_save_when_commit_is_false(self):
        self.assertTrue(self.form.is_valid())
        edited_team = self.form.save(commit=False)
        self.assertEqual(edited_team.team_name, self.team.team_name)
        self.assertEqual(edited_team.team_description, self.team.team_description)
        self.assertEqual(edited_team.team_members, self.team.team_members)

    def test_form_invalid_when_user_to_add_does_not_exist(self):
        self.form_input = {
            'team_name': 'Edited Team Name',
            'team_description': 'Edited Team Description',
            'add_members': '@nonexistentuser'
        }
        form = EditTeamForm(data=self.form_input, instance=self.team)

        #self.assertTrue(self.form.is_valid())
        #edited_team = self.form.save()
        #self.assertNotIn('@nonexistentuser', [user.username for user in edited_team.team_members.all()])
        self.assertFalse(form.is_valid())

    def test_form_valid_when_no_user_selected_to_add(self):
        self.form_input['add_members'] = ''
        form = EditTeamForm(data=self.form_input, instance=self.team)
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data.get('add_members'))

    def test_form_valid_when_adding_existing_user_not_in_team(self):
        self.form_input['add_members'] = '@janedoe'
        form = EditTeamForm(data=self.form_input, instance=self.team)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_adding_existing_user_already_in_team(self):
        self.team.team_members.add(self.added_user)
        self.form_input['add_members'] = '@janedoe'
        form = EditTeamForm(data=self.form_input, instance=self.team)
        self.assertFalse(form.is_valid())

    def test_form_saves_team_with_new_member_when_valid(self):
        self.form_input['add_members'] = '@janedoe'
        form = EditTeamForm(data=self.form_input, instance=self.team)
        form.is_valid()
        edited_team = form.save()
        self.assertIn(self.added_user, edited_team.team_members.all())