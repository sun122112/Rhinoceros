"""Unit tests of the create team task view."""
from django.test import TestCase
from django.urls import reverse
from tasks.forms import CreateTaskForm
from tasks.models import Task, Team, User

class CreateTeamTaskViewTestCase(TestCase):
    """Unit tests of the create team task view."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/teams.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.team = Team.objects.get(id=1)
        self.url = reverse('create_team_task', kwargs={'team_id': self.team.id})
        self.form_input = {
            'task_name': 'Test Task B',
            'task_description': 'Test Task B Description',
            'due': '2023-12-30',
            'assigned': self.user.id,
            'status': 'not_started',
        }

    def test_create_team_task_url(self):
        self.assertEqual(self.url, f'/dashboard/create_task/{self.team.id}/')

    def test_get_create_team_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')

    def test_successful_valid_create_team_task(self):
        """Form submitted with valid data, User redirected correctly, Message works correctly."""
        
        response = self.client.post(self.url, data=self.form_input, follow=True)
        response_url = reverse('team_info', kwargs={'team_id': self.team.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Team Task Created!")
        self.assertTrue(Task.objects.filter(task_name='Test Task B').exists())

    def test_successful_create_team_task(self):
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('team_info', kwargs={'team_id': self.team.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'team_info.html')

    def test_unsuccessful_create_team_task(self):
        self.form_input['task_name'] = ''
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertTrue(form.is_bound)