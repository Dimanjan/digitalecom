# Integration Tests

This folder contains integration tests that make actual API calls to test the full system.

**Note: These tests require the backend and frontend servers to be running.**

## Setup

1. Start the backend server:
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

2. Start the frontend server (optional, for frontend tests):
```bash
cd frontend
npm run dev
```

## Running Tests

### Backend API Integration Tests
```bash
cd integration_tests
python -m pytest backend_api_tests.py -v
```

### Frontend API Integration Tests
```bash
cd integration_tests
npm test
```

## Cleanup

After testing is complete, you can delete this entire folder:
```bash
rm -rf integration_tests
```

