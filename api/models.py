from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Створюємо власний менеджер, який працює тільки з email
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email є обов\'язковим полем')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Наша оновлена модель Користувача
class User(AbstractUser):
    username = None  # Вимикаємо стандартний логін
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    
    GENDER_CHOICES = [
        ('M', 'Чоловіча'),
        ('F', 'Жіноча'),
        ('O', 'Інша'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Стать")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата народження")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Вказуємо використовувати наш новий менеджер!
    objects = CustomUserManager()

    def __str__(self):
        return self.email

# 2. Модель "Про додаток"
class AppInfo(models.Model):
    name = models.CharField(max_length=100, default="Battleship API", verbose_name="Назва додатку")
    description = models.TextField(verbose_name="Опис")
    logo = models.URLField(help_text="Посилання на картинку емблеми", verbose_name="Емблема (URL)")

    def __str__(self):
        return self.name

# 3. Модель "Гра Морський Бій"
class Game(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Очікування суперника'),
        ('active', 'В процесі'),
        ('finished', 'Завершена'),
    ]

    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE, verbose_name="Гравець 1")
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Гравець 2")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Статус")
    
    # JSON поля для зберігання стану дошки
    player1_ships = models.JSONField(default=dict, blank=True, verbose_name="Кораблі Гравця 1")
    player2_ships = models.JSONField(default=dict, blank=True, verbose_name="Кораблі Гравця 2")
    player1_shots = models.JSONField(default=list, blank=True, verbose_name="Постріли Гравця 1")
    player2_shots = models.JSONField(default=list, blank=True, verbose_name="Постріли Гравця 2")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        p2_name = self.player2.name if self.player2 else 'Очікування'
        return f"Гра {self.id}: {self.player1.name} vs {p2_name}"