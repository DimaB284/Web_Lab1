from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, AppInfo, Game
from .serializers import RegisterSerializer, UserProfileSerializer, AppInfoSerializer

# Обов'язкові функції [cite: 23, 24]
class AppInfoView(generics.RetrieveAPIView):
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer
    def get_object(self):
        return AppInfo.objects.first()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

# Робоча функція додатка: Постріл у Морському Бою [cite: 27, 39]
@api_view(['POST'])
def make_shot(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        coordinate = request.data.get('coordinate')
        
        # Записуємо постріл
        game.player1_shots.append(coordinate)
        game.save()
        
        return Response({
            "status": "success",
            "shot": coordinate,
            "message": "Постріл зафіксовано"
        })
    except Game.DoesNotExist:
        return Response({"error": "Гру не знайдено"}, status=404)