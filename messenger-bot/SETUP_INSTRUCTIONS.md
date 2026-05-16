# Messenger Announcement Bot - Setup Guide

## Step 1: Create Facebook App & Get Messenger Tokens

### 1.1 Create a Facebook Business Account
- Go to https://business.facebook.com
- Sign up or log in with your Facebook account

### 1.2 Create an App
1. Go to https://developers.facebook.com/apps/
2. Click "Create App"
3. Choose "Business" as the app type
4. Fill in app name (e.g., "Announcement Bot")
5. Accept terms and create the app

### 1.3 Add Messenger Product
1. In your app dashboard, click "Add Product"
2. Find "Messenger" and click "Set Up"
3. Choose how to set up (select "App or Page")

### 1.4 Get Your Tokens
1. Go to **Settings → Basic** in your app
   - Copy your **App ID** and **App Secret** (save these!)

2. Go to **Messenger → Settings**
   - You'll generate a **Page Access Token** (needed to add as a page manager)

3. Generate **Webhook Verify Token** (you create this)
   - This can be any random string, e.g., `your_webhook_verify_token_123`

### 1.5 Connect to a Facebook Page
1. Go to **Messenger → Settings**
2. Under "Access Tokens", select a Facebook Page
3. Click "Generate Token" - this is your **Page Access Token**
4. Copy and save this token (you'll need it in the bot)

**If you don't have a Facebook Page:**
- Go to https://business.facebook.com/creation
- Create a page for your business/project
- Use that page in step 1.5

### 1.6 Get Group IDs
1. Open your Messenger group in Facebook
2. Look at the URL or open the group info
3. Find the Group ID (or the bot will auto-detect them)

---

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Requirements include:**
- Flask (web framework)
- APScheduler (job scheduling)
- Requests (HTTP requests to Messenger API)
- Flask-SQLAlchemy (database)

---

## Step 3: Configure the Bot

### Create `.env` file in project root:
```
PAGE_ACCESS_TOKEN=your_page_access_token_here
APP_SECRET=your_app_secret_here
WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token_123
FLASK_SECRET_KEY=your_secret_key_here_change_this
DATABASE_URL=sqlite:///announcements.db
```

**Where to get these:**
- `PAGE_ACCESS_TOKEN` → Step 1.5 (Messenger Settings)
- `APP_SECRET` → Step 1.4 (App Settings → Basic)
- `WEBHOOK_VERIFY_TOKEN` → You create this (any random string)
- `FLASK_SECRET_KEY` → Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## Step 4: Run the Bot

```bash
python main.py
```

The bot will start on `http://localhost:5000`

---

## Step 5: Set Up Webhook (For Live Messages)

### Option A: Using ngrok (For Local Testing)
```bash
# Install ngrok from https://ngrok.com/
ngrok http 5000
```

This gives you a public URL like: `https://abc123.ngrok.io`

### Option B: Deploy to a Server
- Use Heroku, Railway, PythonAnywhere, or AWS
- Get a permanent public URL

### Configure Webhook in Facebook
1. Go to your app → **Messenger → Settings**
2. Under "Webhook URL", enter: `https://your-public-url/webhook`
3. Verify Token: Enter your `WEBHOOK_VERIFY_TOKEN`
4. Click "Verify and Save"

5. Under "Webhook Fields", subscribe to:
   - `messages`
   - `messaging_postbacks`

---

## Step 6: Add Bot to Groups

1. Go to your Facebook Page
2. Find the groups where you want to post
3. Add the bot/page as a member (or the bot will auto-add itself)
4. The bot will auto-detect groups and list them in the dashboard

---

## Dashboard Access

Once running, open: **http://localhost:5000**

### Features:
- ✅ View all groups the bot is in
- ✅ Create new announcements
- ✅ Schedule announcements with date, time, and frequency
- ✅ Edit/delete scheduled announcements
- ✅ View announcement history
- ✅ Test send announcements immediately

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid token" | Check your PAGE_ACCESS_TOKEN in .env |
| Bot not in groups | Add the page/bot to groups manually first |
| Webhook not verifying | Ensure WEBHOOK_VERIFY_TOKEN matches in Facebook settings |
| Scheduler not running | Check console for errors, restart with `python main.py` |
| 404 on dashboard | Make sure you're accessing `http://localhost:5000` not another port |

---

## Security Notes

- Never commit `.env` file to git
- Keep your tokens secret
- Use a strong `FLASK_SECRET_KEY`
- For production, use environment variables

---

## Next Steps

1. Complete Steps 1-3 above
2. Run the bot: `python main.py`
3. Open dashboard at http://localhost:5000
4. Create and schedule your first announcement!

Need help? Check the console output for specific error messages.
