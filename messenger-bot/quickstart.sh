#!/bin/bash

# Messenger Bot - Quick Start Script (Unix/Linux/macOS)
# This script automates the setup process

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Messenger Bot - Quick Start Setup                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check Redis
echo "🔍 Checking Redis installation..."
if ! command -v redis-server &> /dev/null; then
    echo "⚠️  Redis is not installed. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install redis
    else
        sudo apt-get install -y redis-server
    fi
fi
echo "✅ Redis found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Facebook credentials!"
    echo ""
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Migrations completed"
echo ""

# Create superuser
echo "👤 Creating superuser..."
echo "Enter superuser details (you'll be prompted):"
python manage.py createsuperuser
echo "✅ Superuser created"
echo ""

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput
echo "✅ Static files collected"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Setup Complete! ✅                                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit .env file with your Facebook credentials"
echo "   nano .env"
echo ""
echo "2. Open 4 terminals and run these commands:"
echo ""
echo "   Terminal 1 (Django):"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "   Terminal 2 (Redis):"
echo "   redis-server"
echo ""
echo "   Terminal 3 (Celery Worker):"
echo "   source venv/bin/activate"
echo "   celery -A config worker --loglevel=info"
echo ""
echo "   Terminal 4 (Celery Beat):"
echo "   source venv/bin/activate"
echo "   celery -A config beat --loglevel=info"
echo ""
echo "3. Open http://localhost:8000 in your browser"
echo ""
echo "4. Login and add your messenger groups!"
echo ""
echo "📚 Full setup guide: SETUP_GUIDE.md"
echo "❓ Questions? Check README.md"
echo ""
