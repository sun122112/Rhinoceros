"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User, Task

class TaskModelTestCase(TestCase):
    """Unit tests for the Task model."""


    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/tasks.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.task = Task.objects.get(id=1)


    def test_valid_task(self):
        self._assert_task_is_valid()

    def test_task_name_cannot_be_blank(self):
        self.task.task_name = ''
        self._assert_task_is_invalid()

    def test_task_name_can_be_50_characters_long(self):
        self.task.task_name = 'x' * 50
        self._assert_task_is_valid()

    def test_task_name_cannot_be_over_50_characters_long(self):
        self.task.task_name = 'x' * 51
        self._assert_task_is_invalid()
    
    def test_task_description_can_be_200_characters_long(self):
        self.task.task_description = 'x' * 200
        self._assert_task_is_valid()

    def test_task_description_cannot_be_over_200_characters_long(self):
        self.task.task_description = 'x' * 201
        self._assert_task_is_invalid()

    def test_task_duedate_must_be_a_date(self):
        self.task.due='not a date'
        self._assert_task_is_invalid()

    def test_task_duedate_must_not_be_in_the_past(self):
        self.task.due='2023-10-10'
        self._assert_task_is_invalid()
    
    def test_task_duedate_can_be_the_future_date(self):
        self.task.due='2026-10-10'
        self._assert_task_is_valid()

    def test_task_assigned_can_be_blank(self):
        self.task.assigned=None
        self._assert_task_is_valid()

    def test_task_assigned_must_be_assigned_to_a_user(self):
        with self.assertRaises(ValueError):
            self.task.assigned='not a user'

    def test_task_status_default_is_not_started(self):
        self.task.status='not_started'
        self._assert_task_is_valid()

    def test_task_status_cant_be_blank(self):
        self.task.status=''
        self._assert_task_is_invalid()

    def _assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except (ValidationError):
            self.fail('Test task should be valid')

    def _assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()