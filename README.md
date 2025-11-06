# Digital Products E-Commerce Store

A modern e-commerce platform for selling digital products like ChatGPT, Spotify, and other subscription services. Built with Django REST Framework backend and Next.js frontend.

## Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart functionality
- 💳 Order management
- 🎨 Modern, responsive UI
- 🔍 Product search and filtering
- ✅ Comprehensive test coverage

## Screenshots

### Frontend
![Frontend Showcase](./frontend/app/showcases/frontend.png)

### Backend API
![Backend Showcase](./frontend/app/showcases/backend.png)

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- SQLite (development)

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios

## Project Structure

```
ecomdigitalproducts/
├── backend/          # Django backend
│   ├── ecomdigital/  # Main Django project
│   ├── products/     # Products app
│   ├── orders/       # Orders app
│   └── manage.py
├── frontend/         # Next.js frontend
│   ├── app/          # Next.js app directory
│   ├── components/   # React components
│   ├── lib/          # API utilities
│   └── types/        # TypeScript types
└── README.md
```

## Quick Setup

For automated setup, run:
```bash
./setup.sh
```

This will set up both backend and frontend automatically.

## Manual Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

6. Load sample data:
```bash
python manage.py seed_data
```
This will create sample categories and products including Spotify Premium, ChatGPT Plus, Netflix Premium, and more.

7. Start the development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Running Tests

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/categories/` - List all categories

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Get order details

## Environment Variables

Create a `.env` file in the backend directory (optional for development):
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

For the frontend, you can set:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Admin Access

Access the Django admin panel at `http://localhost:8000/admin` using the superuser credentials created during setup.

## License

MIT

