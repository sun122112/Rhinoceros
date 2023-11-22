'''Configuration of the admin interface for this project.'''
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of admin interface for users."""
    # specify attributes included in table view of users
    list_display = [
        'username', 'first_name', 'last_name' , 'is_active'
    ]