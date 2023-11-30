from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from datetime import timedelta
from django.utils import timezone

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

""" def default_due():
    return timezone.now() + timedelta(days=7) """


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
    #assigned = models.IntegerField(default=1)
    #assigned = models.CharField()
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='assigned')
    #done = models.BooleanField(default=False)
    status = models.IntegerField(default=Status.NOT_STARTED)
