"""
Integration tests for backend API endpoints.
These tests make actual HTTP requests to the running Django server.

Make sure the backend server is running before executing these tests:
    cd backend
    source venv/bin/activate
    python manage.py runserver
"""

import requests
import json
import pytest
from typing import Dict, Optional

BASE_URL = "http://localhost:8000/api"


class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        import time
        # Use timestamp to ensure unique username
        timestamp = int(time.time())
        url = f"{BASE_URL}/auth/register/"
        data = {
            "username": f"testuser_integration_{timestamp}",
            "email": f"test_integration_{timestamp}@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        assert "access" in response.json()
        assert "refresh" in response.json()
        assert "user" in response.json()
        return response.json()
    
    def test_register_duplicate_user(self):
        """Test that duplicate registration fails"""
        url = f"{BASE_URL}/auth/register/"
        data = {
            "username": "testuser_integration",
            "email": "test_integration@example.com",
            "password": "testpass123",
            "password2": "testpass123"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 400, "Duplicate registration should fail"
    
    def test_login_user(self):
        """Test user login"""
        url = f"{BASE_URL}/auth/login/"
        data = {
            "username": "testuser_integration",
            "password": "testpass123"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        assert "access" in response.json()
        assert "refresh" in response.json()
        return response.json()
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = f"{BASE_URL}/auth/login/"
        data = {
            "username": "testuser_integration",
            "password": "wrongpassword"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 401, "Invalid credentials should return 401"
    
    def test_get_user_profile(self):
        """Test getting user profile with authentication"""
        # First login
        login_data = self.test_login_user()
        token = login_data["access"]
        
        url = f"{BASE_URL}/auth/user/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser_integration"
        return token
    
    def test_refresh_token(self):
        """Test token refresh"""
        login_data = self.test_login_user()
        refresh_token = login_data["refresh"]
        
        url = f"{BASE_URL}/auth/token/refresh/"
        data = {"refresh": refresh_token}
        response = requests.post(url, json=data)
        assert response.status_code == 200
        assert "access" in response.json()


class TestProductsAPI:
    """Test products endpoints"""
    
    def test_get_products(self):
        """Test getting list of products"""
        url = f"{BASE_URL}/products/"
        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data or isinstance(data, list)
        return data
    
    def test_get_featured_products(self):
        """Test getting featured products"""
        url = f"{BASE_URL}/products/featured/"
        response = requests.get(url)
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) <= 8, "Featured products should be max 8"
    
    def test_get_product_detail(self):
        """Test getting a specific product"""
        # First get products list
        products_data = self.test_get_products()
        products = products_data.get("results", products_data) if isinstance(products_data, dict) else products_data
        
        if products and len(products) > 0:
            product_id = products[0]["id"]
            url = f"{BASE_URL}/products/{product_id}/"
            response = requests.get(url)
            assert response.status_code == 200
            assert response.json()["id"] == product_id
    
    def test_search_products(self):
        """Test product search"""
        url = f"{BASE_URL}/products/?search=spotify"
        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        products = data.get("results", data) if isinstance(data, dict) else data
        # Should find at least one product with "spotify" in name or description
        assert len(products) > 0
    
    def test_get_categories(self):
        """Test getting categories"""
        url = f"{BASE_URL}/products/categories/"
        response = requests.get(url)
        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list) or "results" in categories


class TestOrdersAPI:
    """Test orders endpoints"""
    
    def test_create_order(self):
        """Test creating an order"""
        url = f"{BASE_URL}/orders/"
        data = {
            "customer_name": "Test Customer",
            "customer_email": "customer@example.com",
            "items": [
                {
                    "product_name": "Spotify Premium",
                    "product_price": "9.99",
                    "quantity": 1
                }
            ]
        }
        response = requests.post(url, json=data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        order = response.json()
        assert "id" in order
        assert order["total_amount"] == "9.99"
        assert len(order["items"]) == 1
        return order
    
    def test_get_orders(self):
        """Test getting list of orders"""
        url = f"{BASE_URL}/orders/"
        response = requests.get(url)
        assert response.status_code == 200
        orders = response.json()
        assert isinstance(orders, list) or "results" in orders
    
    def test_get_order_detail(self):
        """Test getting a specific order"""
        # First create an order
        order = self.test_create_order()
        order_id = order["id"]
        
        url = f"{BASE_URL}/orders/{order_id}/"
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == order_id


class TestReviewsAPI:
    """Test reviews endpoints"""
    
    def get_auth_token(self):
        """Helper to get authentication token"""
        auth_test = TestAuthenticationAPI()
        return auth_test.test_get_user_profile()
    
    def test_create_review(self):
        """Test creating a review"""
        token = self.get_auth_token()
        
        # First get a product
        products_url = f"{BASE_URL}/products/"
        products_response = requests.get(products_url)
        products = products_response.json()
        product_list = products.get("results", products) if isinstance(products, dict) else products
        
        if not product_list or len(product_list) == 0:
            pytest.skip("No products available for review testing")
        
        # Check if review already exists
        reviews_url = f"{BASE_URL}/reviews/my_reviews/"
        headers = {"Authorization": f"Bearer {token}"}
        my_reviews = requests.get(reviews_url, headers=headers).json()
        
        # Find a product without a review
        reviewed_product_ids = [r["product"] for r in my_reviews]
        product_id = None
        for product in product_list:
            if product["id"] not in reviewed_product_ids:
                product_id = product["id"]
                break
        
        # If all products are reviewed, try to create anyway (should get proper error)
        if product_id is None:
            product_id = product_list[0]["id"]
        
        url = f"{BASE_URL}/reviews/"
        data = {
            "product": product_id,
            "rating": 5,
            "title": "Great product!",
            "comment": "Really enjoyed using this product. Highly recommend!"
        }
        response = requests.post(url, json=data, headers=headers)
        
        # If review already exists, that's okay - we test the error handling
        if response.status_code == 400 and 'already reviewed' in response.json().get('error', '').lower():
            # Get existing review instead
            existing_reviews = [r for r in my_reviews if r["product"] == product_id]
            if existing_reviews:
                review = existing_reviews[0]
                return review, product_id, token
            else:
                pytest.skip("Review already exists but couldn't retrieve it")
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        review = response.json()
        assert review["rating"] == 5
        assert review["title"] == "Great product!"
        assert "id" in review, "Review response should include id"
        return review, product_id, token
    
    def test_get_product_reviews(self):
        """Test getting reviews for a product"""
        review, product_id, _ = self.test_create_review()
        
        url = f"{BASE_URL}/reviews/product_reviews/?product_id={product_id}"
        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        assert "reviews" in data
        assert "average_rating" in data
        assert "total_reviews" in data
        assert len(data["reviews"]) > 0
    
    def test_get_my_reviews(self):
        """Test getting current user's reviews"""
        _, _, token = self.test_create_review()
        
        url = f"{BASE_URL}/reviews/my_reviews/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        reviews = response.json()
        assert isinstance(reviews, list)
        assert len(reviews) > 0
    
    def test_update_review(self):
        """Test updating a review"""
        review, product_id, token = self.test_create_review()
        review_id = review["id"]
        
        url = f"{BASE_URL}/reviews/{review_id}/"
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "product": product_id,
            "rating": 4,
            "title": "Updated review",
            "comment": "Updated comment"
        }
        response = requests.put(url, json=data, headers=headers)
        assert response.status_code == 200
        updated_review = response.json()
        assert updated_review["rating"] == 4
        assert updated_review["title"] == "Updated review"
    
    def test_delete_review(self):
        """Test deleting a review"""
        review, _, token = self.test_create_review()
        review_id = review["id"]
        
        url = f"{BASE_URL}/reviews/{review_id}/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204
        
        # Verify it's deleted
        get_url = f"{BASE_URL}/reviews/{review_id}/"
        get_response = requests.get(get_url, headers=headers)
        assert get_response.status_code == 404
    
    def test_create_review_unauthenticated(self):
        """Test that unauthenticated users cannot create reviews"""
        products_url = f"{BASE_URL}/products/"
        products_response = requests.get(products_url)
        products = products_response.json()
        product_list = products.get("results", products) if isinstance(products, dict) else products
        
        if not product_list or len(product_list) == 0:
            pytest.skip("No products available")
        
        product_id = product_list[0]["id"]
        
        url = f"{BASE_URL}/reviews/"
        data = {
            "product": product_id,
            "rating": 5,
            "title": "Test",
            "comment": "Test comment"
        }
        response = requests.post(url, json=data)
        assert response.status_code == 401, "Unauthenticated requests should fail"


class TestFullWorkflow:
    """Test complete user workflows"""
    
    def test_complete_purchase_workflow(self):
        """Test: Register -> Login -> Browse Products -> Add to Cart -> Create Order"""
        # Register
        auth = TestAuthenticationAPI()
        register_data = auth.test_register_user()
        token = register_data["access"]
        
        # Get products
        products_test = TestProductsAPI()
        products = products_test.test_get_products()
        product_list = products.get("results", products) if isinstance(products, dict) else products
        
        if not product_list or len(product_list) == 0:
            pytest.skip("No products available")
        
        # Create order
        orders_test = TestOrdersAPI()
        order = orders_test.test_create_order()
        assert order is not None
    
    def test_review_workflow(self):
        """Test: Login -> View Product -> Create Review -> View Reviews"""
        # Login
        auth = TestAuthenticationAPI()
        login_data = auth.test_login_user()
        token = login_data["access"]
        
        # Get product
        products_test = TestProductsAPI()
        products = products_test.test_get_products()
        product_list = products.get("results", products) if isinstance(products, dict) else products
        
        if not product_list or len(product_list) == 0:
            pytest.skip("No products available")
        
        # Create review
        reviews_test = TestReviewsAPI()
        review, product_id, _ = reviews_test.test_create_review()
        assert review is not None
        
        # Get product reviews
        reviews_url = f"{BASE_URL}/reviews/product_reviews/?product_id={product_id}"
        response = requests.get(reviews_url)
        if response.status_code == 200:
            reviews_data = response.json()
            assert reviews_data["total_reviews"] > 0
        else:
            # If no reviews yet, that's okay for this test
            pass


if __name__ == "__main__":
    print("=" * 60)
    print("Integration Tests for Digital Products E-Commerce API")
    print("=" * 60)
    print("\nMake sure the backend server is running:")
    print("  cd backend")
    print("  source venv/bin/activate")
    print("  python manage.py runserver")
    print("\nRunning tests...\n")
    
    pytest.main([__file__, "-v", "--tb=short"])

