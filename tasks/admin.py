'''Configuration of the admin interface for this project.'''
from django.contrib import admin

from .models import User, Task, Team


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of admin interface for users."""
    # specify attributes included in table view of users
    list_display = [
        'username', 'first_name', 'last_name', 'is_active'
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configuration of admin interface for tasks."""
    list_display = [
        'task_name', 'task_description', 'due', 'assignor', 'assigned_to', 'status'
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuration of admin interface for teams."""
    list_display = [
        'team_name', 'team_description'
    ]
