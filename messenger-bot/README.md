# Messenger Bot

A Django web application that lets you schedule announcements and send them to Facebook Messenger groups.

## Features
- Create, edit, delete announcements with flexible scheduling (once, daily, weekly, monthly).
- Manage Messenger groups you own.
- View logs of sent announcements.
- **Free‑tier cloud deployment** on Render – no local process needed.
- **Cron‑based sending**: a lightweight `/cron/trigger‑announcements/<secret>/` endpoint that Render (or any free cron service) can hit every minute to dispatch pending announcements.

## Tech Stack
- Django 5.x
- PostgreSQL (Neon) – free tier
- Redis (Upstash) – for optional caching / Celery fallback (now unused)
- WhiteNoise for static files
- Rest Framework for API endpoints

## Setup (local development)
```bash
# Clone the repo
git clone https://github.com/rahiq-rahman/Messenger-Bot.git
cd Messenger-Bot/messenger-bot

# Create virtual environment & install deps
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Create .env (copy from .env.example) and fill in your keys
cp .env.example .env
# edit .env – set DATABASE_URL, REDIS_URL, FACEBOOK_PAGE_ACCESS_TOKEN, etc.

# Run migrations & start server
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the dashboard.

## Deploy to Render (free tier)
1. Create a **Web Service** on Render pointing to the repository.
2. Set the **Build Command** to:
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   ```
3. Set the **Start Command** to:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
   ```
4. Add the following **Environment Variables** (from your `.env`):
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DATABASE_URL`
   - `REDIS_URL`
   - `FACEBOOK_PAGE_ACCESS_TOKEN`
   - `FACEBOOK_VERIFY_TOKEN`
   - `ALLOWED_HOSTS` (your Render domain)
   - `CRON_SECRET_KEY` (a random secret, e.g. `a1b2c3d4`)
5. Deploy – Render will automatically rebuild on pushes.

## Cron‑Based Announcement Dispatch (Free‑Tier Solution)
Render’s free tier does **not** run background workers, so we expose a secure endpoint that a free cron service can call.

### Endpoint
```
GET/POST https://<your‑render‑app>.onrender.com/cron/trigger-announcements/<CRON_SECRET_KEY>/
```
- Returns `200` with JSON `{"status":"success"}` after processing pending announcements.
- If the secret key is wrong, returns `403`.

### Set up a free cron service (e.g., https://cron-job.org/)
1. Create a new cron job.
2. Set the URL to the endpoint above, using the same secret you placed in `.env`.
3. Schedule it to run **every minute**.
4. Enable *Ignore SSL errors* if you use a custom domain without HTTPS (Render provides HTTPS by default).

## Removing Celery (what we did)
- Deleted `@shared_task` decorators from `messenger_bot/tasks.py` and made the functions synchronous.
- Updated `views.py` to import and call `send_scheduled_announcements()` directly.
- Added `trigger_announcements` view (CSRF‑exempt) that calls the same logic.
- Added URL pattern `cron/trigger-announcements/<secret>/`.
- Added `CRON_SECRET_KEY` env variable for simple authentication.
- Updated `.env` with the new secret.
- (Celery config lines remain but are harmless; the app no longer relies on a worker.)

## License
MIT License – feel free to fork, modify, and deploy.
