from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time

class MessengerGroup(models.Model):
    """Model to store Messenger groups where bot is added"""
    group_id = models.CharField(max_length=255, unique=True)
    group_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messenger_groups')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = "Messenger Groups"


class Announcement(models.Model):
    """Model to store announcement messages"""
    FREQUENCY_CHOICES = [
        ('once', 'One Time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='once')
    scheduled_date = models.DateField(null=True, blank=True, help_text="Date for one-time announcements")
    scheduled_time = models.TimeField(default=time(9, 0), help_text="Time to send announcement (HH:MM format)")
    
    # For recurring announcements
    days_of_week = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Comma-separated: Mon,Tue,Wed,Thu,Fri,Sat,Sun (for weekly)"
    )
    day_of_month = models.IntegerField(null=True, blank=True, help_text="Day of month (1-31) for monthly announcements")
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    groups = models.ManyToManyField(MessengerGroup, related_name='announcements')
    
    is_active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Announcements"

    def should_send_today(self):
        """Check if announcement should be sent today"""
        from datetime import datetime, date, timedelta

        if not self.is_active:
            return False

        today = date.today()
        now = timezone.now()
        current_time = now.time()
        current_hour = now.hour
        current_minute = now.minute
        scheduled_hour = self.scheduled_time.hour
        scheduled_minute = self.scheduled_time.minute

        # Check if scheduled time has passed in current timezone
        time_passed = (current_hour > scheduled_hour) or (current_hour == scheduled_hour and current_minute >= scheduled_minute)

        if not time_passed:
            return False

        # Check if already sent today
        if self.last_sent:
            last_sent_date = self.last_sent.astimezone(timezone.get_current_timezone()).date()
            if last_sent_date == today:
                return False

        if self.frequency == 'once':
            return self.scheduled_date == today

        elif self.frequency == 'daily':
            return True

        elif self.frequency == 'weekly':
            days = [d.strip().lower() for d in self.days_of_week.split(',')]
            today_name = today.strftime('%A').lower()
            return today_name in days

        elif self.frequency == 'monthly':
            return today.day == self.day_of_month

        return False


class AnnouncementLog(models.Model):
    """Log of sent announcements for tracking and debugging"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='logs')
    group = models.ForeignKey(MessengerGroup, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ], default='pending')
    error_message = models.TextField(blank=True)
    messenger_timestamp = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.announcement.title} -> {self.group.group_name} ({self.sent_at})"

    class Meta:
        verbose_name_plural = "Announcement Logs"
        ordering = ['-sent_at']
