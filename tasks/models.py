from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from libgravatar import Gravatar


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)


class Task(models.Model):
    class Status(models.IntegerChoices):
        NOT_STARTED = 0, 'Not Started'
        IN_PROGRESS = 1, 'In Progress'
        DONE = 2, 'Done'

    task_name = models.CharField(max_length=32)
    task_description = models.CharField(max_length=200)
    due = models.DateField(blank=True, null=True)
    # order = models.IntegerField()
    assignor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='given_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='received_tasks')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_STARTED)
    # done = models.BooleanField(default=False)


class Team(models.Model):
    team_name = models.CharField(max_length=32)
    team_description = models.CharField(max_length=200)
    # team_members =
