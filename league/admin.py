from django.contrib import admin

from league.models import User, Coach, Team, Player
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(Player)
