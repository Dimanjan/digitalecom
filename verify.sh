#!/bin/bash

echo "========================================="
echo "Verifying E-Commerce Digital Products Store"
echo "========================================="
echo ""

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found"
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check backend Python files
echo "Checking backend files..."
if [ -f "backend/manage.py" ] && [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend files present"
else
    echo "❌ Backend files missing"
    exit 1
fi

# Check frontend package.json
echo "Checking frontend files..."
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend files present"
else
    echo "❌ Frontend files missing"
    exit 1
fi

echo ""
echo "========================================="
echo "Setup Instructions:"
echo "========================================="
echo ""
echo "Backend:"
echo "  1. cd backend"
echo "  2. python3 -m venv venv"
echo "  3. source venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. python manage.py migrate"
echo "  6. python manage.py seed_data"
echo "  7. python manage.py runserver"
echo ""
echo "Frontend:"
echo "  1. cd frontend"
echo "  2. npm install"
echo "  3. npm run dev"
echo ""
echo "Tests:"
echo "  Backend: cd backend && python manage.py test"
echo "  Frontend: cd frontend && npm test"
echo ""
echo "========================================="

