from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

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
        NOT_STARTED = 0
        IN_PROGRESS = 1
        DONE = 2

    task_name = models.CharField(max_length=32)
    task_description = models.CharField(max_length=200)
    #due = models.DateTimeField(default=default_due)
    due = models.DateField(blank=True, null=True)
    #order = models.IntegerField()
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='assigned')
    #done = models.BooleanField(default=False)
    status = models.IntegerField(default=Status.NOT_STARTED)

class Team(models.Model):
    team_name = models.CharField(max_length=32)
    team_description = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='teams')

class Invitation(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient_username = models.CharField(max_length=255)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, default=1)


    def __str__(self):
        return f"Invitation from {self.sender.username} to {self.recipient_username} for {self.invited_user.username}"