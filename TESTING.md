# Testing Documentation

This document describes the comprehensive test suite for the Digital Products E-Commerce Store.

## Test Structure

### Backend Tests (Django)

All backend tests are located in the respective app's `tests.py` files:

- `backend/products/tests.py` - Product and Category tests
- `backend/orders/tests.py` - Order and OrderItem tests
- `backend/authentication/tests.py` - Authentication and user management tests
- `backend/reviews/tests.py` - Review and rating tests

### Frontend Tests (Jest + React Testing Library)

All frontend tests are located in `__tests__` directories:

- `frontend/components/__tests__/` - Component tests
- `frontend/app/__tests__/` - Page tests (if needed)

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
python manage.py test
```

Run specific test files:
```bash
python manage.py test products.tests
python manage.py test authentication.tests
python manage.py test reviews.tests
python manage.py test orders.tests
```

Run all tests with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests

```bash
cd frontend
npm test
```

Run tests in watch mode:
```bash
npm run test:watch
```

Run tests with coverage:
```bash
npm test -- --coverage
```

## Test Coverage

### Backend Test Coverage

#### Products App
- ✅ Category model creation and validation
- ✅ Product model creation and relationships
- ✅ Product API endpoints (list, detail, featured, search)
- ✅ Category API endpoints
- ✅ Product filtering and pagination

#### Orders App
- ✅ Order model creation
- ✅ OrderItem model creation
- ✅ Order API endpoints (create, list, detail)
- ✅ Order total calculation
- ✅ Order item relationships

#### Authentication App
- ✅ User registration with validation
- ✅ User login with JWT tokens
- ✅ Token refresh functionality
- ✅ User profile retrieval
- ✅ User profile update
- ✅ Password validation
- ✅ Authentication required endpoints

#### Reviews App
- ✅ Review model creation
- ✅ Review uniqueness (one per user per product)
- ✅ Review API endpoints (create, list, update, delete)
- ✅ Product reviews aggregation
- ✅ Average rating calculation
- ✅ Rating validation (1-5 stars)
- ✅ User's own reviews endpoint

### Frontend Test Coverage

#### Components
- ✅ ProductCard component rendering
- ✅ Navbar component with authentication state
- ✅ ReviewList component with reviews display
- ✅ ReviewForm component with submission
- ✅ Authentication context provider

#### Pages
- ✅ Home page with featured products
- ✅ Products listing page
- ✅ Product detail page
- ✅ Cart page
- ✅ Login page
- ✅ Register page
- ✅ Profile page

## Test Organization

### Backend Test Classes

1. **Model Tests** - Test model creation, validation, and relationships
2. **API Tests** - Test API endpoints, serializers, and permissions
3. **Integration Tests** - Test complete workflows

### Frontend Test Suites

1. **Component Tests** - Test component rendering and interactions
2. **Integration Tests** - Test component interactions with API
3. **Context Tests** - Test React context providers

## Writing New Tests

### Backend Test Example

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class MyModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Setup test data
    
    def test_model_creation(self):
        # Test model creation
        pass
    
    def test_api_endpoint(self):
        # Test API endpoint
        response = self.client.get(reverse('endpoint-name'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Frontend Test Example

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import MyComponent from '../MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
  
  it('handles user interaction', () => {
    render(<MyComponent />)
    fireEvent.click(screen.getByRole('button'))
    // Assert expected behavior
  })
})
```

## Continuous Integration

Tests should be run automatically on:
- Pull requests
- Commits to main branch
- Before deployment

## Test Best Practices

1. **Isolation**: Each test should be independent
2. **Setup/Teardown**: Use setUp and tearDown methods
3. **Naming**: Use descriptive test names
4. **Coverage**: Aim for >80% code coverage
5. **Speed**: Keep tests fast (< 1 second per test)
6. **Mocking**: Mock external dependencies
7. **Assertions**: Use clear, specific assertions

## Known Issues

None at this time.

## Future Test Improvements

- [ ] Add E2E tests with Playwright or Cypress
- [ ] Add performance tests
- [ ] Add load testing
- [ ] Add security tests
- [ ] Increase test coverage to >90%

