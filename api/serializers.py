from rest_framework import serializers
from .models import User, AppInfo

class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = ['name', 'description', 'logo']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'gender', 'date_of_birth', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            gender=validated_data.get('gender'),
            date_of_birth=validated_data.get('date_of_birth'),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'gender', 'date_of_birth']