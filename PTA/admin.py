'''

Rahul Soni, Psyrs11

This file tells Django which models need to be accessible by the admin page outside of the defaults like User.


'''

from django.contrib import admin
from .models import Trade, Institution, Party
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from PTA.models import Profile

admin.site.register(Trade)

admin.site.register(Institution)

admin.site.register(Party)

'''

This class exists so that there will be a dropdown box in the User creation/modification screen that will allow profile
information (the institution) to be changed from the admin page. It is required because profile is a separate model,
and making a separate creation page would be tedious and counter intuitive.

'''
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin, adds the above class to the page
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin with the profile field added
admin.site.unregister(User)
admin.site.register(User, UserAdmin)