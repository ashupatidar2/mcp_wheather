#!/bin/bash

echo "🎨 Starting Frontend Server..."
echo "================================"

cd "$(dirname "$0")/frontend"

echo "🌐 Frontend will run on: http://localhost:3000"
echo "================================"
echo ""
echo "💡 Make sure backend is running on http://localhost:8000"
echo "   Run './run_backend.sh' in another terminal"
echo ""
echo "🌐 Open your browser and go to: http://localhost:3000"
echo ""

# Start simple HTTP server
python3 -m http.server 3000
