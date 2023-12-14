"""Unit tests of the edit task form."""
from django import forms
from django.test import TestCase
from tasks.forms import EditTaskForm
from tasks.models import User, Task


class EditTaskFormTestCase(TestCase):
    """Unit tests of the edit task form."""

    fixtures = ['tasks/tests/fixtures/default_user.json', 'tasks/tests/fixtures/tasks.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.task = Task.objects.get(pk=1)
        self.form_input = {
            'task_name': 'Update task',
            'task_description': 'This is a test task.',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'done',
        }
        self.form = EditTaskForm(data=self.form_input, instance=self.task)

    def test_form_accepts_valid_input(self):
        self.assertTrue(self.form.is_valid())

    def test_form_rejects_blank_task_name(self):
        self.form_input['task_name'] = ''
        self.assertFalse(self.form.is_valid())

    def test_form_rejects_blank_task_description(self):
        self.form_input['task_description'] = ''
        self.assertFalse(self.form.is_valid())

    def test_form_rejects_invalid_due_date(self):
        self.form_input['due'] = 'invalid due'
        self.assertFalse(self.form.is_valid())

    def test_can_save_valid_task(self):
        self.assertTrue(self.form.is_valid())
        update_task = self.form.save()
        self.assertEqual(update_task.task_name, self.form_input['task_name'])
        self.assertEqual(update_task.task_description, self.form_input['task_description'])
        self.assertEqual(update_task.due.strftime('%Y-%m-%d'), self.form_input['due'])
        self.assertEqual(update_task.assigned, self.user)
        self.assertEqual(update_task.status, self.form_input['status'])

    def test_edit_task_form_does_not_save_when_commit_is_false(self):
        self.assertTrue(self.form.is_valid())
        update_task = self.form.save(commit=False)
        self.assertEqual(update_task.task_name, self.task.task_name)
        self.assertEqual(update_task.task_description, self.task.task_description)
        self.assertEqual(update_task.due, self.task.due)
        self.assertEqual(update_task.assigned, self.task.assigned)
        self.assertEqual(update_task.status, self.task.status)


