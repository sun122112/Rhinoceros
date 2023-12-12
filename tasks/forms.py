"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Task, Team , Invitation
from django.contrib import messages

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user

class CreateTaskForm(forms.ModelForm):
    """Form enabling users to create new tasks, regardless of if a team has been registered or not."""

    class Meta:
        """Form options"""

        model = Task
        fields = ['task_name', 'task_description', 'due', 'assigned', 'status']
        widgets = {'task_description': forms.Textarea(), 'assigned': forms.Select(), 'status': forms.Select()}

    def save(self, commit=True):
        """Saving a newly created task"""

        super().save(commit=False)
        task=Task(
            task_name=self.cleaned_data.get('task_name'),
            task_description=self.cleaned_data.get('task_description'),
            due=self.cleaned_data.get('due'),
            assigned=self.cleaned_data.get('assigned'),
            status=self.cleaned_data.get('status')
        )
        if commit:
            task.save()

        return task

class CreateTeamForm(forms.ModelForm):
    """Form enabling users to create new teams"""

    class Meta:
        """Form options"""

        model = Team
        fields = ['team_name', 'team_description']
        widgets = {'team_description' : forms.Textarea()}

    def save(self, commit = True):
        """Saving a newly created team"""

        super().save(commit=False)
        team=Team(
            team_name=self.cleaned_data.get('team_name'),
            team_description=self.cleaned_data.get('team_description'),

        )
        if commit:
            team.save()

        return team
<<<<<<< HEAD
    
class InvitationForm(forms.Form):
    username = forms.CharField(label='Username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
=======

class EditTeamForm(forms.ModelForm):
    """Form enabling users to edit teams"""

    add_members = forms.CharField(label='Add team member', widget=forms.TextInput(attrs={'placeholder':'Enter username'}),required=False)
    #current_members=forms.CharField(widget=forms.Textarea(attrs=('readonly': 'readonly')), required=True)

    class Meta:
        """Form options"""

        model=Team
        fields = ['team_name', 'team_description']
        widgets = {'team_description' : forms.Textarea()}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team=self.instance
        
    
    def save(self, commit=True):
        self.team.name=self.cleaned_data.get('team_name')
        self.team.description=self.cleaned_data.get('team_description')

        add_members_username = self.cleaned_data.get('add_members')
        

        user_to_add = User.objects.filter(username=add_members_username).first()
        if user_to_add is not None:
            self.team.team_members.add(user_to_add)
 

        if commit:
            self.team.save()
        return self.team


class EditTaskForm(forms.ModelForm):
    """Form enabling users to edit task"""

    class Meta:
        """Form options"""

        model = Task
        fields = ['task_name', 'task_description', 'due', 'assigned', 'status']
        widgets = {'task_description': forms.Textarea(), 'assigned': forms.Select(), 'status': forms.Select()}

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task=self.instance
        
    
    def save(self, commit=True):
        self.task.name=self.cleaned_data.get('task_name')
        self.task.description=self.cleaned_data.get('task_description')

        if commit:
            self.task.save()
        return self.task
>>>>>>> origin/dashboard_interface
