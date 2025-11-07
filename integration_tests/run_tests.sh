#!/bin/bash

echo "========================================="
echo "Running Integration Tests"
echo "========================================="
echo ""

# Check if backend is running
echo "Checking if backend server is running..."
if curl -s http://localhost:8000/api/products/ > /dev/null; then
    echo "✅ Backend server is running"
else
    echo "❌ Backend server is not running!"
    echo "Please start it with:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python manage.py runserver"
    exit 1
fi

echo ""
echo "========================================="
echo "Running Backend API Tests (Python)"
echo "========================================="
echo ""

cd "$(dirname "$0")"

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run Python tests
python -m pytest backend_api_tests.py -v --tb=short

PYTHON_EXIT_CODE=$?

echo ""
echo "========================================="
echo "Running Frontend API Tests (Node.js)"
echo "========================================="
echo ""

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Run Node.js tests
npm test

NODE_EXIT_CODE=$?

echo ""
echo "========================================="
echo "Test Results Summary"
echo "========================================="
echo ""

if [ $PYTHON_EXIT_CODE -eq 0 ] && [ $NODE_EXIT_CODE -eq 0 ]; then
    echo "✅ All integration tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    echo "Python tests exit code: $PYTHON_EXIT_CODE"
    echo "Node.js tests exit code: $NODE_EXIT_CODE"
    exit 1
fi

