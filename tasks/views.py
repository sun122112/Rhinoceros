from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
<<<<<<< HEAD
from .models import Team
from django.shortcuts import render, get_object_or_404 ##
from django.views.generic.edit import FormView, UpdateView, DeleteView
=======
#from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import FormView, UpdateView, DeleteView, DetailView

>>>>>>> origin/dashboard_interface
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, CreateTaskForm, CreateTeamForm, EditTeamForm, EditTaskForm
from tasks.helpers import login_prohibited
from .models import Invitation
from .forms import InvitationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import ListView

from django.http import HttpResponse
from tasks.models import User, Task, Team
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

    tasks = Task.objects.filter(assigned=current_user, team__isnull=True)
    return render(request, 'my_tasks.html', {'user': current_user, 'tasks': tasks})


class TeamListView(ListView):
    model = Team
    template_name = 'my_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)


class TeamDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)
        return self.request.user in team.members.all() or self.request.user == team.creator

@login_required
def my_teams(request):
    """page to view my teams"""
    current_user = request.user
    teams = Team.objects.filter(team_members__in=[current_user])
    return render(request, 'my_teams.html', {'teams': teams})

def view_team_members(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.members.all():
        return HttpResponseForbidden("You are not authorized to view this team.")

    team_members = team.members.all()
    return render(request, 'view_team_members.html', {'team': team, 'team_members': team_members})

    """team = Team.objects.get(id=team_id)
    team_members = team.members.all()
    return render(request, 'view_team_members.html', {'team': team, 'team_members': team_members})"""\

def accept_invitation(request, invitation_id):
    
    invitation = Invitation.objects.get(id=invitation_id)

    user = request.user
    team = invitation.team 

    team.members.add(user)

    invitation.status = Invitation.Status.ACCEPTED
    invitation.save()

    messages.success(request, f"You have accepted the invitation to join {team.team_name}")

    return redirect('my_teams')

def invite_users(request, team_id):
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            try:
                invited_user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, f'User with username {username} does not exist.')
                return redirect('my_teams')

            if invited_user in team.members.all():
                messages.info(request, f'{invited_user.username} is already a member of the team.')
                return redirect('my_teams')

            existing_invitation = Invitation.objects.filter(team=team, invited_user=invited_user)
            if existing_invitation.exists():
                messages.info(request, f'Invitation already sent to {invited_user.username}.')
                return redirect('my_teams')

            invitation = Invitation(team=team, invited_user=invited_user, sender=request.user)
            invitation.save()

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
    invitation = Invitation.objects.get(id=invitation_id)

    user = request.user
    team = invitation.team
    team.members.add(user)

    team.members.add(user)

    invitation.status = Invitation.Status.ACCEPTED
    invitation.save()

    messages.success(request, f"You have accepted the invitation to join {team.team_name}")

    return redirect('my_teams')

@login_required
def team_join(request, team_id):
    team = get_object_or_404(Team, id=team_id)

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
        task.assigned = self.request.user
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
        self.task = Task.objects.get(id=self.kwargs.get('task_id'))
        return self.task

    def get_success_url(self):
        """Return redirect URL after successful deletion"""
        
        if self.task.team:
            messages.add_message(self.request, messages.ERROR, "Team Task Deleted!")
            return reverse('team_info', kwargs={'team_id': self.task.team_id})
        elif self.task.team == None:
            messages.add_message(self.request, messages.ERROR, "Task Deleted!")
            return reverse('my_tasks')



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
    success_url = reverse_lazy('my_teams')


    def form_valid(self, form):
        team = form.save(commit=False)
        
        team.save()
        team.team_members.add(self.request.user) 
        self.object = team
        team.members.add(self.request.user)
        form.save_m2m()
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

class EditTeamView(FormView):
    
    model=Team
    template_name ="edit_team.html"
    form_class = EditTeamForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'instance': self.get_object(self.kwargs.get('team_id'))})
        return kwargs
    
    def get_object(self, team_id):
        """Return team, as a object, to be edited"""
        team = Team.objects.get(id=team_id)
        return team

    def get_success_url(self):
        """Return redirect URL after successful edit"""
        messages.add_message(self.request, messages.SUCCESS, "Team Details Updated!")
        return reverse('my_teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs.get('team_id')
        context['team'] = Team.objects.get(id=team_id)
        return context  
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)


class TeamInfoView(DetailView):
    """Display team info"""
    model = Team
    template_name = "team_info.html"



    def get(self,request,team_id):
        current_user=request.user
        team = Team.objects.get(id=team_id)
        tasks= Task.objects.filter(team=team)
        return render(request, 'team_info.html', {'user': current_user, 'tasks': tasks, 'team':team})

class CreateTeamTaskView(FormView):
    """Display a create task view and handle newly created tasks for a specific team. """
    form_class = CreateTaskForm
    template_name= "create_task.html"
  
    def form_valid(self, form):
        team_id=self.kwargs.get('team_id')
        team=Team.objects.get(id=team_id)

        task = form.save(commit=False)
        task.team= team
        task.assigned = self.request.user
        task.save()
        self.object = task

        return super().form_valid(form)
    


    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Team Task Created!")
        team_id=self.kwargs.get('team_id')

        return reverse('team_info', kwargs={'team_id': team_id})

    def get_form(self, form_class=form_class):
        form=super().get_form(form_class)
        members = Team.objects.get(
            id=self.kwargs.get('team_id')).team_members.all()

        form.fields['assigned'].queryset = members

        return form

    def get_context_data(self, **kwargs:Any):
        context = super().get_context_data(**kwargs)
        context['team_id'] =self.kwargs.get('team_id')
        return context

class EditTaskView(FormView):
    
    model=Task
    template_name ="edit_task.html"
    form_class = EditTaskForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'instance': self.get_object(self.kwargs.get('task_id'))})
        return kwargs
    
    def get_object(self, task_id):
        self.task = Task.objects.get(id=task_id)
        return self.task

    def get_success_url(self):
        """Return redirect URL after successful edit of either team tasks or personal tasks"""

        if self.task.team:
            messages.add_message(self.request, messages.SUCCESS, "Team Task Details Updated!")
            return reverse('team_info', kwargs={'team_id': self.task.team_id})
        elif self.task.team == None:
            messages.add_message(self.request, messages.SUCCESS, "Task Details Updated!")
            return reverse('my_tasks')


    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('task_id')
        context['task'] = Task.objects.get(id=task_id)
        return context  
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)