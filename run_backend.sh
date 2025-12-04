#!/bin/bash

echo "🚀 Starting Backend Server..."
echo "================================"

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ -d "../venv" ]; then
    echo "📦 Activating virtual environment..."
    source ../venv/bin/activate
fi

# Install dependencies if needed
if [ ! -f ".dependencies_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch .dependencies_installed
fi

echo "🌐 Backend will run on: http://localhost:8000"
echo "📡 API Documentation: http://localhost:8000/docs"
echo "================================"
echo ""

# Start the server
python main.py
