"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import view_team_members, invite_users
from tasks.views import view_invitations
from tasks.views import accept_invitation
from tasks.views import TeamListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('dashboard/create_task/', views.CreateTaskView.as_view(), name='create_task'),
    path('dashboard/delete_task/<int:task_id>/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('dashboard/my_tasks/', views.my_tasks, name='my_tasks'),
    path('dashboard/my_teams/', views.my_teams, name='my_teams'),
    path('dashboard/create_team/', views.CreateTeamView.as_view(), name='create_team'),
    path('view_team_members/<int:team_id>/', view_team_members, name='view_team_members'),
    path('invite_users/<int:team_id>/', views.invite_users, name='invite_users'),
    path('team_join/<int:team_id>/', views.team_join, name='team_join'),
    path('view_invitations/', view_invitations, name='view_invitations'),
    path('dashboard/delete_team/<int:team_id>/', views.DeleteTeamView.as_view(), name='delete_team'),
    path('dashboard/my_teams/team_info/<int:team_id>/', views.TeamInfoView.as_view(), name='team_info'),
    path('dashboard/my_teams/edit_team/<int:team_id>/', views.EditTeamView.as_view(), name='edit_team'),
    path('dashboard/create_task/<int:team_id>/', views.CreateTeamTaskView.as_view(), name='create_team_task'),
    path('dashboard/my_tasks/edit_task/<int:task_id>/', views.EditTaskView.as_view(), name='edit_task'),
]
