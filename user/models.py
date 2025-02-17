from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
import os
from uuid import uuid4
from allauth.account.models import EmailAddress
from django.db import models
from datetime import timedelta
from datetime import date,timedelta

class CustomUserManager(BaseUserManager):
    """
    Create and return a regular user with the given email and password.
    """
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(email, password, **extra_fields)
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        # Remove Profile.objects.create() from here since signal will handle it
        return user


class CustomUser(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    last_seen=models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects=CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username=models.CharField(max_length=32)
    bio=models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    # Level and Experience
    level = models.PositiveIntegerField(default=1)
    current_xp = models.PositiveIntegerField(default=0)
    total_xp_earned = models.PositiveIntegerField(default=0)  # Total XP ever earned
    xp_to_next_level = models.PositiveIntegerField(default=100)  # XP needed for next level

    # Learning Stats
    study_streak = models.PositiveIntegerField(default=0)  # Consecutive days of learning
    last_study_date = models.DateField(null=True, blank=True)
    total_study_sessions = models.PositiveIntegerField(default=0)
    total_study_time = models.DurationField(default=timedelta(seconds=0))  # Total time spent learning

    # Achievement and Progress
    quizzes_completed = models.PositiveIntegerField(default=0)
    quizzes_score_avg = models.FloatField(default=0.0)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def calculate_xp_to_next_level(self):
        """Calculate XP needed for next level using a progression formula"""
        base_xp = 100
        multiplier = 1.5
        return int(base_xp * (multiplier ** (self.level)))

    def add_xp(self, amount):
        """Add XP and handle level up logic"""
        self.current_xp += amount
        self.total_xp_earned += amount

        while self.current_xp >= self.xp_to_next_level:
            self.current_xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = self.calculate_xp_to_next_level()

    def update_streak(self):
        """Update study streak based on last_study_date"""
        today = date.today()

        if self.last_study_date == today - timedelta(days=1):
            self.study_streak += 1
        elif self.last_study_date != today:
            self.study_streak = 1

        self.last_study_date = today
        self.save()


class StudySession(models.Model):
    CATEGORY_CHOICES = [
        ('reading', 'Reading'),
        ('practice', 'Practice'),
        ('video', 'Video Lecture'),
        ('quiz', 'Quiz'),
        ('other', 'Other'),
    ]
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #it will be in seconds
    duration=models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    quiz_score = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.duration} sec)"

    def calculate_xp(self):
        """Calculate XP based on duration (e.g., 10 XP per minute)"""
        return (self.duration // 60) * 5  # 5 XP per minute

    def save(self, *args, **kwargs):
        """Automatically update XP earned before saving"""
        self.xp_earned = self.calculate_xp()
        super().save(*args, **kwargs)