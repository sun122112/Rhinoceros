from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Task, Team

import pytz
from faker import Faker
from random import randint, random

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    DEFAULT_PASSWORD = 'Password123'

    TASK_COUNT = 200
    TEAM_COUNT = 100

    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.create_teams()
        self.teams= Team.objects.all()
        self.create_tasks()
        self.tasks= Task.objects.all()
        

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )

    def create_tasks(self):
        self.generate_task_fixtures()
        self.generate_random_tasks()

    def generate_task_fixtures(self):
        for data in task_fixtures:
            self.try_create_task(data)

    def generate_random_tasks(self):
        task_count = Task.objects.count()
        while  task_count < self.TASK_COUNT:
            print(f"Seeding task {task_count}/{self.TASK_COUNT}", end='\r')
            self.generate_task()
            task_count = Task.objects.count()
        print("Task seeding complete.      ")

    def generate_task(self):
        task_name = self.faker.sentences(nb_words=10)
        task_description = self.faker.paragraph(nb_sentences=3)
        due = self.faker.future_date(end_date='+365d')
        assigned = self.users.order_by('?').first()
        status = self.faker.random_element(elements=('not_started', 'in_progress', 'done'))
        team = self.teams.order_by('?').first() if random.random() < 0.5 else None

        self.try_create_task({
            'task_name': task_name,
            'task_description': task_description,
            'due': due,
            'assigned': assigned,
            'status': status,
            'team': team,
        })

    def try_create_task(self, data):
        try:
            self.create_task(data)
        except:
            pass

    def create_task(self, data):
        Task.objects.create(
            task_name=data['task_name'],
            task_description=data['task_description'],
            due=data['due'],
            assigned=data['assigned'],
            status=data['status'],
            team=data['team'],
        )

    def create_teams(self):
        self.generate_team_fixtures()
        self.generate_random_teams()

    def generate_team_fixtures(self):
        for data in team_fixtures:
            self.try_create_team(data)

    def generate_random_teams(self):
        team_count = Team.objects.count()
        while team_count < self.TEAM_COUNT:
            print(f"Seeding team {team_count}/{self.TEAM_COUNT}", end='\r')
            self.generate_team()
            team_count = Team.objects.count()
        print("Team seeding complete.      ")

    def generate_team(self):
        team_name = self.faker.sentence(nb_words=2)
        team_description = self.faker.text(max_nb_chars=200)
        team_members = self.users.order_by('?')[:randint(1, 10)] 

        self.try_create_team({
            'team_name': team_name,
            'team_description': team_description,
            'team_members': team_members,
        })

    def try_create_team(self, data):
        try:
            self.create_team(data)
        except:
            pass

    def create_team(self, data):
        team = Team.objects.create(
            team_name=data['team_name'],
            team_description=data['team_description'],
        )
        team.team_members.set(data['team_members'])


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'


