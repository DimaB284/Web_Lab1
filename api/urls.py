from django.urls import path
from .views import RegisterView, UserProfileView, AppInfoView, make_shot

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('about/', AppInfoView.as_view(), name='about'),
    path('game/<int:game_id>/shot/', make_shot, name='make-shot'),
]