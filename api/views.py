from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, AppInfo, Game
from .serializers import RegisterSerializer, UserProfileSerializer, AppInfoSerializer

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
            "message": "Shot has been completed!"
        })
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=404)