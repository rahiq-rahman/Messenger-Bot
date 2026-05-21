# Celery Setup & Message Scheduling Guide

## Why Messages Aren't Being Sent

Messages don't send because **Celery workers and Beat scheduler aren't running**. You need to start them manually.

---

## Prerequisites

1. ✅ Redis server is running (already configured at `rediss://vital-akita-131190.upstash.io:6379`)
2. ✅ Python dependencies installed (`celery`, `redis`, `django-celery-beat`)
3. ✅ Facebook Page Access Token configured in `.env`

---

## How to Run (3 Terminal Windows)

### Terminal 1: Run Django Development Server
```bash
cd messenger-bot
python manage.py runserver
```
Access at: http://localhost:8000

---

### Terminal 2: Run Celery Worker
This executes the actual tasks:
```bash
cd messenger-bot
celery -A config worker -l info
```

Expected output:
```
celery@YOUR-PC ready to accept tasks
```

---

### Terminal 3: Run Celery Beat (Scheduler)
This triggers tasks at scheduled times:
```bash
cd messenger-bot
celery -A config beat -l info
```

Expected output:
```
celery beat v5.x.x started
Scheduler: django_celery_beat.schedulers.DatabaseScheduler
```

---

## Verify It's Working

### 1. Check Celery Worker is receiving tasks
- Look at Terminal 2 (Celery Worker) for activity
- Should show: `[tasks] Received task: messenger_bot.tasks.send_scheduled_announcements`

### 2. Check Django Logs
- Open `messenger-bot/logs/` directory
- Look for log files with send attempts

### 3. Test with a Manual Task
Run this in Django shell to test sending:
```bash
python manage.py shell
```
```python
from messenger_bot.tasks import send_to_group
from messenger_bot.models import Announcement, MessengerGroup

# Test with your first announcement and group
ann = Announcement.objects.first()
group = MessengerGroup.objects.first()

if ann and group:
    send_to_group.delay(ann.id, group.id)
    print("Test task queued!")
```

---

## Common Issues & Fixes

### ❌ "ConnectionError: Error 111 connecting to localhost:6379"
**Problem:** Redis connection failed
**Solution:** Your Redis URL in `.env` is already set to Upstash. Make sure you have internet connection.

### ❌ "Access Denied to FACEBOOK_PAGE_ACCESS_TOKEN"
**Problem:** Facebook token is placeholder
**Solution:** 
1. Get real token from Facebook Developer Dashboard
2. Replace in `.env`:
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=your_real_token_here
   ```

### ❌ "Scheduled task runs but message doesn't send"
**Problem:** Facebook API error
**Solution:**
1. Check logs in Django console
2. Verify token has correct permissions
3. Make sure bot is added to Facebook group
4. Check group ID is correct (should be numeric)

### ❌ "Messages say 'Pending' forever"
**Problem:** Celery worker crashed
**Solution:** 
1. Restart Terminal 2 (Celery Worker)
2. Clear pending tasks: `celery -A config purge` (careful - removes all tasks)

---

## Message Status Guide

| Status | Meaning | Action |
|--------|---------|--------|
| **Pending** | Task waiting in queue | Celery worker must be running |
| **Success** | Message sent to Facebook | Check Facebook group |
| **Failed** | API error or token invalid | Check error message & logs |

---

## How Scheduling Works

1. **Every minute:** Celery Beat runs `send_scheduled_announcements`
2. **Check each announcement:** Uses `should_send_today()` to check if it's time to send
3. **Send if needed:** Queues message sending task
4. **Celery Worker:** Picks up task and sends via Facebook API
5. **Log result:** Creates entry in dashboard logs

### Example Timeline
```
1:00 PM - Beat: "Check announcements"
         → Found "Daily standup" scheduled for 1:00 PM today ✓
         → Queued send task
         
1:00:05 PM - Worker picks up task
         → Sends message to all groups
         → Logs: "success" or "failed"
         
1:00:10 PM - Dashboard shows in Logs page
```

---

## For Production (Advanced)

### Option 1: Systemd Services (Linux)
Create service files to auto-start on boot:
- `celery-worker.service`
- `celery-beat.service`

### Option 2: Docker
Use Docker Compose to manage all services:
- Django
- Celery Worker
- Celery Beat
- Redis

### Option 3: Cloud Services
- **DigitalOcean App Platform**
- **Render**
- **Railway**
(All have built-in Redis and background workers)

---

## Monitoring

### View Active Tasks
```bash
celery -A config inspect active
```

### View Scheduled Tasks
```bash
celery -A config inspect scheduled
```

### Clear Queue
```bash
celery -A config purge
```

---

## Quick Troubleshooting Checklist

- [ ] Django server running? (Terminal 1)
- [ ] Celery worker running? (Terminal 2)
- [ ] Celery beat running? (Terminal 3)
- [ ] Facebook token set in .env? (Not placeholder)
- [ ] Redis connection working? (Check Terminal 2/3 startup)
- [ ] Announcement is_active = True?
- [ ] Group is_active = True?
- [ ] Current time >= scheduled_time?
- [ ] Correct day? (For weekly/monthly)

---

## Support

Check these for error details:
1. Terminal 1 (Django) - Application errors
2. Terminal 2 (Worker) - Task execution errors
3. Terminal 3 (Beat) - Scheduling errors
4. Dashboard Logs - Final status & Facebook API errors
