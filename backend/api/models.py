from django.db import models

# Create your models here.

class Influencer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    content_type = models.JSONField()  # Store multiple content types
    collaboration_history = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
    ]

    influencer = models.ForeignKey(
        Influencer,
        related_name='social_accounts',
        on_delete=models.CASCADE
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    username = models.CharField(max_length=100)
    followers_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
