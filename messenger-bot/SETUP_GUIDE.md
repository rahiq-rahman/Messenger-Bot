# Messenger Bot - Complete Setup Guide

## Overview
This is a Django-based Messenger Bot that allows you to schedule and send announcements to Facebook Messenger groups.

## Features
- ✅ Schedule announcements for multiple groups
- ✅ Multiple frequency options (One-time, Daily, Weekly, Monthly)
- ✅ Web dashboard for easy management
- ✅ Automatic sending via Celery scheduler
- ✅ Detailed logging and tracking
- ✅ User authentication and multi-user support

---

## Prerequisites

1. **Python 3.8+**
2. **Redis Server** (for Celery task queue)
3. **Facebook Business Account** with Messenger API access
4. **PostgreSQL** (optional, SQLite works for testing)

---

## Step 1: Install Required Software

### Windows / macOS / Linux

#### Python
```bash
# Check if Python is installed
python --version

# Install from python.org if needed
```

#### Redis
**Windows:**
- Download from: https://github.com/microsoftarchive/redis/releases
- Or use WSL2: `wsl sudo apt-get install redis-server`

**macOS:**
```bash
brew install redis
```

**Linux:**
```bash
sudo apt-get install redis-server
```

---

## Step 2: Setup Django Project

### 1. Clone/Create Project Directory
```bash
mkdir messenger-bot
cd messenger-bot
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Project Structure
Create this folder structure:
```
messenger-bot/
├── config/
│   ├── __init__.py
│   ├── settings.py (use provided settings.py)
│   ├── urls.py (use provided urls.py)
│   ├── wsgi.py
│   └── asgi.py
├── messenger_bot/
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── announcements/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── groups/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   └── logs.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py (use provided models.py)
│   ├── views.py (use provided views.py)
│   ├── urls.py
│   ├── forms.py (use provided forms.py)
│   ├── serializers.py (use provided serializers.py)
│   ├── tasks.py (use provided tasks.py)
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env
└── db.sqlite3
```

### 5. Create Django App
```bash
python manage.py startapp messenger_bot
```

### 6. Copy Provided Files
- Copy `settings.py` to `config/settings.py`
- Copy `urls.py` to `config/urls.py`
- Copy `models.py` to `messenger_bot/models.py`
- Copy `views.py` to `messenger_bot/views.py`
- Copy `forms.py` to `messenger_bot/forms.py`
- Copy `serializers.py` to `messenger_bot/serializers.py`
- Copy `tasks.py` to `messenger_bot/tasks.py`
- Create templates directory and copy all template files

### 7. Create .env File
Create `.env` in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-this
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

---

## Step 3: Get Facebook Messenger API Credentials

### 1. Create Facebook Business Account
- Visit: https://business.facebook.com
- Create a new business account

### 2. Create a Facebook App
- Go to: https://developers.facebook.com/apps
- Click "Create App"
- Choose "Business" as app type
- Fill in app details

### 3. Add Messenger Product
- In your app dashboard, click "Add Product"
- Search for "Messenger"
- Click "Set Up"

### 4. Get Page Access Token
- In Messenger settings, go to "Access Tokens"
- Select your page
- Copy the Page Access Token
- Add to `.env`: `FACEBOOK_PAGE_ACCESS_TOKEN=your_token`

### 5. Set Verify Token
- Create a random string for verification
- Add to `.env`: `FACEBOOK_VERIFY_TOKEN=random_string`

### 6. Configure Webhook
- In Messenger settings, go to "Webhooks"
- Callback URL: `https://yourdomain.com/webhook/`
- Verify Token: Same as `FACEBOOK_VERIFY_TOKEN`
- Subscribe to: `messages`, `messaging_postbacks`

---

## Step 4: Database Setup

### 1. Make Migrations
```bash
python manage.py makemigrations
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

---

## Step 5: Running the Bot

### Terminal 1: Django Development Server
```bash
python manage.py runserver
```
Access at: http://localhost:8000

### Terminal 2: Redis Server
```bash
redis-server
```

### Terminal 3: Celery Worker
```bash
celery -A config worker --loglevel=info
```

### Terminal 4: Celery Beat (Scheduler)
```bash
celery -A config beat --loglevel=info
```

---

## Step 6: Add Bot to Groups

1. Go to your Facebook Group
2. Add the Facebook Page as a member
3. In the bot dashboard, create the group entry with the Group ID
4. The bot will now be able to send messages

---

## Usage Guide

### 1. Register & Login
- Visit http://localhost:8000
- Create a new account
- Login

### 2. Add Messenger Groups
- Go to "Groups" tab
- Click "Add Group"
- Enter Facebook Group ID and name
- Save

### 3. Create Announcements
- Go to "Announcements" tab
- Click "Create New"
- Fill in details:
  - Title
  - Message
  - Frequency (Daily/Weekly/Monthly/One-time)
  - Time to send
  - Select groups
- Save

### 4. Monitor Logs
- Go to "Logs" tab
- View all sent announcements
- Check status (Success/Failed/Pending)

---

## Deployment Guide

### Using Gunicorn + Nginx

#### 1. Install Production Server
```bash
pip install gunicorn
```

#### 2. Create systemd Service File
Create `/etc/systemd/system/messenger-bot.service`:
```ini
[Unit]
Description=Messenger Bot Django Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/messenger-bot
ExecStart=/path/to/messenger-bot/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3. Start Service
```bash
sudo systemctl start messenger-bot
sudo systemctl enable messenger-bot
```

#### 4. Configure Nginx
Create `/etc/nginx/sites-available/messenger-bot`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/messenger-bot/staticfiles/;
    }
}
```

#### 5. Enable SSL
```bash
sudo certbot --nginx -d yourdomain.com
```

---

## Troubleshooting

### Issue: Redis Connection Error
```
Fix: Make sure Redis is running
redis-server
```

### Issue: Celery Tasks Not Running
```
Fix: Check Celery Beat is running
celery -A config beat --loglevel=info
```

### Issue: Announcements Not Sending
1. Check the LOGS page for errors
2. Verify Facebook Access Token in .env
3. Ensure bot is added to the group
4. Check Celery worker logs

### Issue: "Invalid verification token"
- Make sure FACEBOOK_VERIFY_TOKEN matches in .env and Facebook app settings

---

## API Endpoints

### REST API
- `GET/POST /api/announcements/` - List/Create announcements
- `GET/PUT/DELETE /api/announcements/{id}/` - Manage single announcement
- `POST /api/announcements/{id}/toggle_active/` - Toggle active status
- `GET /api/groups/` - List groups
- `POST /api/groups/` - Create group
- `GET /api/logs/` - View logs

### Webhook
- `POST /webhook/` - Facebook Messenger webhook

---

## Security Notes

1. **Change SECRET_KEY** in production
2. **Use HTTPS** for all connections
3. **Set DEBUG=False** in production
4. **Use strong database passwords**
5. **Rotate Facebook Access Tokens regularly**
6. **Enable CSRF protection** (enabled by default)

---

## Support & Updates

For issues or feature requests:
1. Check the logs page
2. Review Celery worker output
3. Check Django debug mode error pages

---

## License

This project is provided as-is for educational and personal use.

---

## Quick Reference

| Task | Command |
|------|---------|
| Run server | `python manage.py runserver` |
| Run migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Run Celery worker | `celery -A config worker --loglevel=info` |
| Run Celery beat | `celery -A config beat --loglevel=info` |
| Collect static files | `python manage.py collectstatic` |
