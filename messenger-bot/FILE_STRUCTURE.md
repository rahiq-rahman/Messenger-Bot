# Messenger Bot - Complete File Structure

This document describes all files in the Messenger Bot project and their purposes.

## 📂 Project Structure

```
messenger-bot/
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 ✅ Django settings (environment variables, apps, etc.)
│   ├── urls.py                     ✅ Main URL configuration
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── messenger_bot/                   # Main Django app
│   ├── migrations/                 # Database migrations
│   │   └── __init__.py
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html               ✅ Base template with navbar
│   │   ├── login.html              ✅ Login page
│   │   ├── register.html           ✅ Registration page
│   │   ├── dashboard.html          ✅ Main dashboard
│   │   ├── logs.html               ✅ Activity logs page
│   │   │
│   │   ├── announcements/
│   │   │   ├── list.html           ✅ Announcements list
│   │   │   ├── form.html           ✅ Create/edit announcement form
│   │   │   └── confirm_delete.html ✅ Delete confirmation
│   │   │
│   │   └── groups/
│   │       ├── list.html           ✅ Groups list
│   │       ├── form.html           ✅ Create/edit group form
│   │       └── confirm_delete.html ✅ Delete confirmation
│   │
│   ├── __init__.py
│   ├── admin.py                    ✅ Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── models.py                   ✅ Database models
│   ├── views.py                    ✅ View functions and API endpoints
│   ├── forms.py                    ✅ Django forms
│   ├── serializers.py              ✅ REST API serializers
│   ├── tasks.py                    ✅ Celery tasks
│   ├── tests.py                    # Unit tests
│   └── urls.py                     # App URL configuration
│
├── manage.py                        # Django management script
├── celery.py                        ✅ Celery configuration
├── requirements.txt                 ✅ Python dependencies
├── .env.example                     ✅ Environment variables template
├── .env                             # Environment variables (create from .env.example)
├── Dockerfile                       ✅ Docker container configuration
├── docker-compose.yml               ✅ Docker Compose for all services
├── quickstart.sh                    ✅ Quick setup script (Unix/Linux/macOS)
├── quickstart.bat                   ✅ Quick setup script (Windows)
├── README.md                        ✅ Project overview and guide
├── SETUP_GUIDE.md                   ✅ Detailed setup instructions
└── db.sqlite3                       # SQLite database (created after setup)
```

## 📋 File Descriptions

### Core Configuration Files

#### `config/settings.py` ✅
- Django project settings
- Database configuration
- Installed apps configuration
- Celery and Redis settings
- Facebook API configuration
- Static files and media configuration
- Email settings
- **What it does**: Configures entire Django project

#### `config/urls.py` ✅
- Main URL routing
- Includes app URLs
- Admin panel routes
- API endpoints routing
- Messenger webhook endpoint
- **What it does**: Routes all incoming URLs to appropriate views

#### `celery.py` ✅
- Celery task scheduling configuration
- Task routing and timing
- Queue configuration
- **What it does**: Configures Celery for scheduled announcements

### Models & Database

#### `messenger_bot/models.py` ✅
Contains three main models:

1. **MessengerGroup**
   - Fields: group_id, group_name, owner, is_active
   - Stores Facebook groups the bot can send to

2. **Announcement**
   - Fields: title, message, frequency, scheduled_date, scheduled_time, etc.
   - Stores announcement configurations
   - Supports: one-time, daily, weekly, monthly scheduling
   - Many-to-many relationship with MessengerGroups

3. **AnnouncementLog**
   - Fields: announcement, group, sent_at, status, error_message
   - Logs every announcement sent
   - Tracks success/failure/pending status

### Views & Business Logic

#### `messenger_bot/views.py` ✅
- **Authentication Views**: login, register, logout
- **Dashboard View**: Main dashboard with statistics
- **Announcement Views**: List, create, edit, delete announcements
- **Group Views**: List, create, edit, delete groups
- **Logs View**: View sending history
- **Messenger Webhook**: Handles incoming messages from Facebook
- **REST API ViewSets**: API endpoints for all models

#### `messenger_bot/tasks.py` ✅
- **send_scheduled_announcements()**: Checks and sends due announcements
- **send_announcement_to_groups()**: Routes announcement to all groups
- **send_to_group()**: Sends single announcement via Facebook API
- **send_messenger_message()**: Makes actual API call to Facebook
- Handles logging and error tracking

### Forms & Serializers

#### `messenger_bot/forms.py` ✅
- **MessengerGroupForm**: Form for adding/editing groups
- **AnnouncementForm**: Form for creating announcements
- Form validation for different frequency types
- Custom clean() methods for cross-field validation

#### `messenger_bot/serializers.py` ✅
- **MessengerGroupSerializer**: REST API serializer for groups
- **AnnouncementSerializer**: REST API serializer for announcements
- **AnnouncementLogSerializer**: REST API serializer for logs
- Validation and data formatting

#### `messenger_bot/admin.py` ✅
- Django admin interface configuration
- Customized list displays
- Search and filter options
- Read-only fields
- Fieldsets organization
- **What it does**: Makes database editable through Django admin

### Templates (HTML)

#### Base Template
- **`templates/base.html`** ✅
  - Master template with navbar and sidebar
  - Bootstrap 5 styling
  - CSS variables for theming
  - Message display
  - Menu navigation

#### Authentication Templates
- **`templates/login.html`** ✅
  - Login form with username/password
  - Link to registration

- **`templates/register.html`** ✅
  - Registration form
  - Username, email, password fields
  - Link to login

#### Dashboard Templates
- **`templates/dashboard.html`** ✅
  - Statistics cards (announcements, groups, logs)
  - Quick actions buttons
  - Recent activity table
  - Getting started guide

- **`templates/logs.html`** ✅
  - Detailed announcement logs table
  - Status indicators
  - Error messages display
  - Statistics summary

#### Announcement Templates
- **`templates/announcements/list.html`** ✅
  - Grid view of all announcements
  - Shows frequency, groups, last sent
  - Edit/delete buttons for each

- **`templates/announcements/form.html`** ✅
  - Create/edit announcement form
  - Conditional fields based on frequency
  - Groups multi-select
  - Help panel with examples
  - JavaScript for dynamic field visibility

- **`templates/announcements/confirm_delete.html`** ✅
  - Delete confirmation dialog
  - Shows announcement details
  - Confirm/cancel buttons

#### Group Templates
- **`templates/groups/list.html`** ✅
  - Table of all groups
  - Shows announcements count
  - Edit/delete buttons
  - Instructions for finding group ID

- **`templates/groups/form.html`** ✅
  - Create/edit group form
  - Group ID and name fields
  - Help panel with instructions
  - How to find group ID guide

- **`templates/groups/confirm_delete.html`** ✅
  - Delete confirmation for groups
  - Shows group details
  - Warning about announcements

### Setup & Configuration Files

#### `requirements.txt` ✅
Python package dependencies:
- Django & DRF (web framework)
- django-celery-beat (scheduler)
- celery & redis (task queue)
- requests (HTTP library)
- psycopg2 (PostgreSQL driver)
- gunicorn (production server)
- python-dotenv (environment variables)

#### `.env.example` ✅
Environment variables template:
- Django settings (DEBUG, SECRET_KEY)
- Database configuration
- Redis URL
- Facebook API tokens
- Email settings
- Timezone

#### `Dockerfile` ✅
Docker container setup:
- Python 3.11 base image
- Installs system dependencies
- Copies code and installs Python packages
- Exposes port 8000
- Runs gunicorn

#### `docker-compose.yml` ✅
Complete stack with:
- PostgreSQL database
- Redis cache/broker
- Django web server
- Celery worker
- Celery beat scheduler
- Nginx reverse proxy (optional)
- Volume and network configuration

### Scripts

#### `quickstart.sh` ✅
Automated setup for Unix/Linux/macOS:
- Checks Python installation
- Creates virtual environment
- Installs dependencies
- Creates .env file
- Runs migrations
- Creates superuser
- Collects static files

#### `quickstart.bat` ✅
Automated setup for Windows:
- Checks Python installation
- Creates virtual environment
- Installs dependencies
- Creates .env file
- Runs migrations
- Creates superuser
- Shows next steps

### Documentation

#### `README.md` ✅
Comprehensive guide including:
- Project overview
- Feature list
- Quick start (5-minute setup)
- Installation instructions
- Configuration details
- Usage guide
- API reference
- Deployment options
- Troubleshooting
- Architecture diagram

#### `SETUP_GUIDE.md` ✅
Detailed setup documentation:
- Prerequisites
- Step-by-step installation
- Facebook API setup
- Database configuration
- Running development servers
- Adding bot to groups
- Usage instructions
- Deployment with systemd
- Nginx configuration
- SSL setup with Let's Encrypt
- Troubleshooting guide
- API endpoint reference

## 🚀 Quick File Reference

### Must-Have Files (Required for running)
- ✅ `settings.py` - Django configuration
- ✅ `models.py` - Database models
- ✅ `views.py` - View logic
- ✅ `tasks.py` - Celery tasks
- ✅ `urls.py` - URL routing
- ✅ `requirements.txt` - Dependencies

### Frontend Files (For web interface)
- ✅ All HTML templates in `templates/` folder
- ✅ `forms.py` - Form rendering

### API Files (For REST API)
- ✅ `serializers.py` - Data serialization
- ✅ Views with REST viewsets

### Setup Files (For initial setup)
- ✅ `.env.example` - Configuration template
- ✅ `quickstart.sh` / `quickstart.bat` - Automated setup
- ✅ `Dockerfile` + `docker-compose.yml` - Container setup

### Documentation
- ✅ `README.md` - Overview and guide
- ✅ `SETUP_GUIDE.md` - Detailed instructions

## 💾 Database Models Relationship

```
MessengerGroup
├── Owned by User
└── Related to Announcements (Many-to-Many)

Announcement
├── Owned by User
├── Many groups (Many-to-Many)
└── Has logs (One-to-Many)

AnnouncementLog
├── Belongs to Announcement (Many-to-One)
├── Belongs to Group (Many-to-One)
└── Tracks sending history
```

## 🔄 Data Flow

1. **User creates announcement** → Form → Model saved
2. **Celery Beat triggers** → Every minute
3. **Check if announcement due** → should_send_today()
4. **Send to all groups** → send_to_group() task
5. **Make Facebook API call** → send_messenger_message()
6. **Log result** → AnnouncementLog saved
7. **User views logs** → Dashboard shows status

## 📱 Template Structure

All templates:
- Extend from `base.html`
- Use Bootstrap 5 classes
- Have responsive design
- Use CSS variables for theming
- Include Font Awesome icons
- Mobile-friendly layout

## 🔐 Security Features

- CSRF protection enabled
- User authentication required (except login/register)
- Permission checks in views
- Input validation on forms
- SQL injection protection via ORM
- Secure password hashing
- Environment variables for secrets

---

## Getting Started

1. **Copy all files** to your project directory
2. **Edit `.env`** with your Facebook credentials
3. **Run quickstart** script for your OS
4. **Follow instructions** in README.md

For detailed setup, see **SETUP_GUIDE.md**

All files marked with ✅ are provided and ready to use!
