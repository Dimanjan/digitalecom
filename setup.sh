#!/bin/bash

echo "========================================="
echo "Setting up Digital Products E-Commerce Store"
echo "========================================="
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Seeding database with sample data..."
python manage.py seed_data

echo "Creating superuser (optional - press Ctrl+C to skip)..."
python manage.py createsuperuser || echo "Superuser creation skipped"

deactivate
cd ..

echo ""
echo "✅ Backend setup complete!"
echo ""

# Frontend setup
echo "Setting up frontend..."
cd frontend

echo "Installing frontend dependencies..."
npm install

cd ..

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start the servers:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Frontend (in a new terminal):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit http://localhost:3000"
echo ""

