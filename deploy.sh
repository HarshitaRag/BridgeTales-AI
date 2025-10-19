#!/bin/bash

# BridgeTales AI Deployment Script
# This script helps you quickly deploy BridgeTales AI

echo "🎪 BridgeTales AI Deployment"
echo "============================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please create a .env file with your AWS credentials."
    echo ""
    echo "Copy env.template to .env and fill in your credentials:"
    echo "  cp env.template .env"
    echo "  nano .env  # or use your favorite editor"
    echo ""
    exit 1
fi

echo "✅ .env file found"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 is installed"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error installing dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Kill any existing server on port 8000
echo ""
echo "🔄 Checking for existing server on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
echo "✅ Port 8000 is clear"

# Start the server
echo ""
echo "🚀 Starting BridgeTales AI Server..."
echo "📍 Server will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 run.py

