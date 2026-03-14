from django.contrib import admin
from .models import User, AppInfo, Game

# Реєструємо наші моделі, щоб вони з'явилися в адмін-панелі
admin.site.register(User)
admin.site.register(AppInfo)
admin.site.register(Game)