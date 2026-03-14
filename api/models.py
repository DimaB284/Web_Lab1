from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a neccesary field!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="Name")
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Sex")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of birth")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class AppInfo(models.Model):
    name = models.CharField(max_length=100, default="Battleship API", verbose_name="App name")
    description = models.TextField(verbose_name="Description")
    logo = models.URLField(help_text="Icon URL", verbose_name="Icon")

    def __str__(self):
        return self.name

class Game(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for opponent'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]

    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE, verbose_name="Player 1")
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Player 2")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Status")
    
    player1_ships = models.JSONField(default=dict, blank=True, verbose_name="Player 1 ships")
    player2_ships = models.JSONField(default=dict, blank=True, verbose_name="Player 2 ships")
    player1_shots = models.JSONField(default=list, blank=True, verbose_name="Player 1 shots")
    player2_shots = models.JSONField(default=list, blank=True, verbose_name="Player 2 shots")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        p2_name = self.player2.name if self.player2 else 'Waiting'
        return f"Game {self.id}: {self.player1.name} vs {p2_name}"