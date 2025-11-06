# Backend API Documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

## API Endpoints

### Products

- `GET /api/products/` - List all active products
- `GET /api/products/featured/` - Get featured products (first 8)
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/categories/` - List all categories
- `GET /api/products/categories/{id}/` - Get category details

Query parameters:
- `search` - Search products by name or description
- `ordering` - Order by `price`, `created_at`, or `name`

### Orders

- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Get order details

Order creation payload:
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "items": [
    {
      "product_name": "Spotify Premium",
      "product_price": "9.99",
      "quantity": 1
    }
  ]
}
```

## Running Tests

```bash
python manage.py test
```

