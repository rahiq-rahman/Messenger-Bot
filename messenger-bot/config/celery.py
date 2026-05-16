import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('messenger_bot')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Optional: Configure task routing
app.conf.task_routes = {
    'messenger_bot.tasks.send_scheduled_announcements': {'queue': 'default'},
    'messenger_bot.tasks.send_announcement_to_groups': {'queue': 'default'},
    'messenger_bot.tasks.send_to_group': {'queue': 'default'},
}

# Task settings
app.conf.task_track_started = True
app.conf.task_time_limit = 30 * 60  # Hard limit
app.conf.task_soft_time_limit = 25 * 60  # Soft limit


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery"""
    print(f'Request: {self.request!r}')
