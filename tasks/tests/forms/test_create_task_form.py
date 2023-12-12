"""Unit tests of the create task form."""
from django import forms
from django.test import TestCase
from tasks.forms import CreateTaskForm
from tasks.models import User, Task

class CreateTaskFormTestCase(TestCase):
    """Unit tests of the create task form."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'task_name': 'Test task',
            'task_description': 'This is a test task.',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'not_started',
        }

    def test_form_contains_required_fields(self):
        form = CreateTaskForm()
        self.assertIn('task_name', form.fields)
        self.assertIn('task_description', form.fields)

    def test_form_accepts_valid_input(self):
        form = CreateTaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_task_name(self):
        self.form_input['task_name'] = ''
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_due_date(self):
        self.form_input['due'] = 'invalid due'
        form = CreateTaskForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_can_save_valid_task(self):
        form = CreateTaskForm(data=self.form_input)
        before_count = Task.objects.count()
        form.save()
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        task = Task.objects.last()
        self.assertIsNotNone(task)
        self.assertEqual(task.task_name, self.form_input['task_name'])
        self.assertEqual(task.task_description, self.form_input['task_description'])
        self.assertEqual(task.due.strftime('%Y-%m-%d'), self.form_input['due'])
        self.assertEqual(task.assigned, self.user)
        self.assertEqual(task.status, self.form_input['status'])
