# 🤖 Messenger Bot - Announcement Scheduler

A powerful Django web application for scheduling and sending automated announcements to Facebook Messenger groups. Schedule announcements for multiple groups with flexible timing options and monitor delivery through a comprehensive dashboard.

## ✨ Features

- **📅 Flexible Scheduling**: Schedule announcements as one-time, daily, weekly, or monthly
- **👥 Multi-Group Support**: Send to multiple groups with different schedules
- **🌐 Web Dashboard**: Beautiful, user-friendly interface to manage everything
- **📊 Activity Logs**: Track all announcements and their delivery status
- **👤 Multi-User**: Multiple users can manage their own announcements
- **🔔 Real-time Scheduling**: Uses Celery for reliable task scheduling
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔒 Secure**: Authentication, CSRF protection, and secure API endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis Server
- Facebook Business Account with Messenger API access

### Installation (5 minutes)

1. **Clone/Download the project**
```bash
git clone <repo-url>
cd messenger-bot
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env File**
```bash
cp .env.example .env
# Edit .env with your Facebook credentials
```

5. **Setup Database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run Development Servers** (in different terminals)
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Redis
redis-server

# Terminal 3: Celery Worker
celery -A config worker --loglevel=info

# Terminal 4: Celery Beat
celery -A config beat --loglevel=info
```

7. **Access Dashboard**
- Open http://localhost:8000
- Login with your credentials
- Go to Groups → Add your Facebook groups
- Create announcements!

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Installation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation instructions.

## ⚙️ Configuration

### Facebook API Setup

1. **Create Business Account**: https://business.facebook.com
2. **Create App**: https://developers.facebook.com/apps
3. **Add Messenger Product**: In app dashboard
4. **Get Access Token**: Messenger → Access Tokens
5. **Set Webhook**: 
   - URL: `https://yourdomain.com/webhook/`
   - Verify Token: Custom string
   - Events: `messages`, `messaging_postbacks`

### Environment Variables

Create `.env` file in project root:

```env
# Django
DEBUG=False
SECRET_KEY=your-random-secret-key

# Facebook
FACEBOOK_PAGE_ACCESS_TOKEN=your_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

## 📖 Usage

### Adding Messenger Groups

1. Navigate to **Groups** tab
2. Click **Add Group**
3. Enter:
   - **Group ID**: The numeric ID from Facebook
   - **Group Name**: A friendly name
4. Click **Save**

**How to find Group ID:**
- Open Facebook Group/Chat in browser
- Look at URL: `facebook.com/groups/123456789/`
- Group ID = `123456789`

### Creating Announcements

1. Go to **Announcements** tab
2. Click **Create New**
3. Fill in:
   - **Title**: Announcement title
   - **Message**: The announcement text
   - **Frequency**: When to send
   - **Time**: What time to send
   - **Groups**: Which groups to send to
4. Click **Create Announcement**

### Scheduling Options

| Frequency | Configuration | Example |
|-----------|---------------|---------|
| **One-time** | Set date | Send once on Jan 15 at 9:00 AM |
| **Daily** | Set time only | Send every day at 9:00 AM |
| **Weekly** | Set days + time | Send Mon/Wed/Fri at 2:30 PM |
| **Monthly** | Set day + time | Send on 15th each month at 8:00 AM |

### Monitoring

1. Go to **Logs** tab
2. View all sent announcements
3. Check status:
   - ✅ **Success**: Delivered
   - ❌ **Failed**: Check error message
   - ⏳ **Pending**: Waiting to send

## 🔌 API Reference

### REST API Endpoints

```
# Announcements
GET    /api/announcements/          - List all
POST   /api/announcements/          - Create new
GET    /api/announcements/{id}/     - Get details
PUT    /api/announcements/{id}/     - Update
DELETE /api/announcements/{id}/     - Delete
POST   /api/announcements/{id}/toggle_active/  - Toggle active

# Groups
GET    /api/groups/                 - List all
POST   /api/groups/                 - Create new
GET    /api/groups/{id}/            - Get details
PUT    /api/groups/{id}/            - Update
DELETE /api/groups/{id}/            - Delete

# Logs
GET    /api/logs/                   - View all logs

# Webhook
POST   /webhook/                    - Facebook Messenger webhook
```

### Example API Request

```bash
curl -X POST http://localhost:8000/api/announcements/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily Standup",
    "message": "Time for standup!",
    "frequency": "daily",
    "scheduled_time": "09:00",
    "group_ids": [1, 2]
  }'
```

## 🚀 Deployment

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Using Heroku

1. Create `Procfile`:
```
web: gunicorn config.wsgi
worker: celery -A config worker
beat: celery -A config beat
release: python manage.py migrate
```

2. Deploy:
```bash
git push heroku main
```

### Using VPS (Ubuntu)

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed systemd setup.

## 🔍 Troubleshooting

### Announcements Not Sending?

1. **Check Celery is running**
   ```bash
   celery -A config worker --loglevel=debug
   ```

2. **Check Logs page** for errors

3. **Verify Facebook token** in .env

4. **Ensure bot is in group** and has permissions

5. **Check Redis connection**
   ```bash
   redis-cli ping
   ```

### Common Issues

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Restart gunicorn, check logs |
| Task queue errors | Restart Redis and Celery |
| "Invalid token" | Regenerate Facebook access token |
| "Group not found" | Verify group ID is correct |
| Tasks not running | Ensure Celery Beat is running |

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## 📊 System Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │
    ┌────▼────────────────┐
    │   Django App        │
    │  (REST API)         │
    │  (Webhooks)         │
    └────┬────────────────┘
         │
    ┌────▼──────────┐
    │   Database    │
    │  (PostgreSQL) │
    └───────────────┘

    ┌──────────────────────┐
    │  Celery Worker       │
    │  (Task Processing)   │
    └─────────┬────────────┘
              │
    ┌─────────▼──────────┐
    │   Celery Beat      │
    │  (Scheduler)       │
    └────────────────────┘
              │
    ┌─────────▼──────────┐
    │  Messenger API     │
    │  (Facebook)        │
    └────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is provided as-is for personal and educational use.

## 💡 Tips & Best Practices

### Scheduling
- Avoid peak hours for group activity
- Test with one group before adding many
- Use 24-hour time format consistently
- Set announcements for working hours

### Messages
- Keep messages concise and clear
- Use markdown if supported by Messenger
- Test message formatting first
- Avoid special characters that might break formatting

### Monitoring
- Check logs regularly for failures
- Review token expiration dates
- Monitor Celery worker health
- Set up alerts for failed deliveries

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Check Django/Celery logs
4. Review Facebook API documentation

---

**Made with ❤️ for automating announcements**
