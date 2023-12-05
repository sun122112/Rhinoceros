from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from .models import Team
from django.shortcuts import render, get_object_or_404 ##
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateTaskForm, CreateTeamForm
from tasks.helpers import login_prohibited
from .models import Invitation
from .forms import InvitationForm

#from datetime import datetime
#from django.db import transaction
from django.http import HttpResponse
from tasks.models import User, Task, Team
#from tasks.models import Task, default_due
#from django.utils.timezone import make_aware
from typing import Any



@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    return render(request, 'dashboard.html', {'user':current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

@login_required
def my_tasks(request):
    """page to view my tasks"""
    current_user = request.user
    #tasks = Task.objects.all().order_by('order')
    tasks = Task.objects.all()
    return render(request, 'my_tasks.html', {'user': current_user, 'tasks': tasks})

@login_required
def my_teams(request):
    """page to view my teams"""
    teams=Team.objects.all()
    return render(request, 'my_teams.html', {'teams': teams})

def view_team_members(request, team_id):
    team = Team.objects.get(id=team_id)
    team_members = team.members.all()
    return render(request, 'view_team_members.html', {'team': team, 'team_members': team_members})

def accept_invitation(request, invitation_id):
    # Retrieve the invitation object
    invitation = Invitation.objects.get(id=invitation_id)

    # Perform any necessary logic for accepting the invitation
    user = request.user
    team = invitation.team  # Use the team field

    team.members.add(user)

    # Mark the invitation as accepted
    invitation.status = Invitation.Status.ACCEPTED
    invitation.save()

    # Success message
    messages.success(request, f"You have accepted the invitation to join {team.team_name}")

    # Redirect to a relevant page
    return redirect('my_teams')

def invite_users(request, team_id):
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Check if the user with the provided username exists
            try:
                invited_user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, f'User with username {username} does not exist.')
                return redirect('my_teams')

            # Check if the user is already a member of the team
            if invited_user in team.members.all():
                messages.info(request, f'{invited_user.username} is already a member of the team.')
                return redirect('my_teams')

            # Check if there is already an invitation for the user
            existing_invitation = Invitation.objects.filter(invited_user=invited_user)
            if existing_invitation.exists():
                messages.info(request, f'Invitation already sent to {invited_user.username}.')
                return redirect('my_teams')

            # Create and save the invitation
            invitation = Invitation(sender=request.user, invited_user=invited_user)
            invitation.save()

            # Add the invited user to the team's members
            team.members.add(invited_user)

            messages.success(request, f'Invitation sent to {invited_user.username}')
            return redirect('my_teams')
    else:
        form = InvitationForm()

    return render(request, 'invite_users.html', {'team': team, 'form': form})


def view_invitations(request):
    user = request.user
    received_invitations = Invitation.objects.filter(invited_user=user)

    return render(request, 'view_invitations.html', {'invitations': received_invitations})

def accept_invitation(request, invitation_id):
    # Retrieve the invitation object
    invitation = Invitation.objects.get(id=invitation_id)

    # Perform any necessary logic for accepting the invitation
    user = request.user
    team = invitation.team
    team.members.add(user)

    team.members.add(user)

    # Mark the invitation as accepted
    invitation.status = Invitation.Status.ACCEPTED
    invitation.save()

    # success message
    messages.success(request, f"You have accepted the invitation to join {team.team_name}")

    # Redirect to a relevant page
    return redirect('my_teams')

@login_required
def team_join(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Add the current user to the team's members
    team.members.add(request.user)

    return render(request, 'team_join.html', {'team': team})

class CreateTaskView(FormView):
    """Display a create task view and handle newly created tasks. """
    form_class = CreateTaskForm
    template_name= "create_task.html"
    #redirect_when_logged_in_url = 'create_task'
    #redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        task = form.save(commit=False)
        #task.assigned = self.request.user

        #task.assigned = 1

        task.save()
        self.object = task
        return super().form_valid(form)
        

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Task Created!")
        return reverse('my_tasks')

    def get_form(self, form_class=form_class):
        form=super().get_form(form_class)
        form.fields['assigned'].queryset = User.objects.filter(
            id=self.request.user.id)
        return form


class DeleteTaskView(DeleteView):
    """Display a confirmation view to delete tasks and handle task deletion."""
    model = Task
    template_name = "delete_task.html"

    def get_object(self, queryset=None):
        """Return task, as a object, to be deleted"""
        task = Task.objects.get(id=self.kwargs.get('task_id'))
        return task

    def get_success_url(self):
        """Return redirect URL after successful deletion"""
        #messages.add_message(self.request, member.SUCCESS, "Task deleted! ") 
        messages.add_message(self.request, messages.ERROR, "Task Deleted!")
        return reverse('my_tasks')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['task_id'] = self.kwargs.get('task_id')
        return context       

class CreateTeamView(FormView):
    """Display a create team view and handle newly created teams. """
    form_class = CreateTeamForm
    template_name= "create_team.html"


    def form_valid(self, form):
        team = form.save(commit=False)
        team.save()
        self.object = team
        return super().form_valid(form)
        

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Team Created!")
        return reverse('my_teams')

class DeleteTeamView(DeleteView):
    """Display a confirmation view to delete teams and handle team deletion."""
    model = Team
    template_name = "delete_team.html"

    def get_object(self, queryset=None):
        """Return team, as a object, to be deleted"""
        team = Team.objects.get(id=self.kwargs.get('team_id'))
        return team

    def get_success_url(self):
        """Return redirect URL after successful deletion"""
        messages.add_message(self.request, messages.ERROR, "Team Deleted!")
        return reverse('my_teams')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['team_id'] = self.kwargs.get('team_id')
        return context  