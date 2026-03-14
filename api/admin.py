from django.contrib import admin
from .models import User, AppInfo, Game

admin.site.register(User)
admin.site.register(AppInfo)
admin.site.register(Game)