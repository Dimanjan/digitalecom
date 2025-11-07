/**
 * Integration tests for frontend API calls.
 * These tests make actual HTTP requests to the running backend server.
 * 
 * Make sure the backend server is running before executing these tests:
 *     cd backend
 *     source venv/bin/activate
 *     python manage.py runserver
 */

import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

describe('Frontend API Integration Tests', () => {
  let authToken: string | null = null
  let testUserId: number | null = null

  beforeAll(async () => {
    // Register a test user
    try {
      const registerResponse = await axios.post(`${API_BASE_URL}/auth/register/`, {
        username: `testuser_${Date.now()}`,
        email: `test_${Date.now()}@example.com`,
        password: 'testpass123',
        password2: 'testpass123',
        first_name: 'Test',
        last_name: 'User'
      })
      authToken = registerResponse.data.access
      testUserId = registerResponse.data.user.id
    } catch (error: any) {
      // User might already exist, try to login
      try {
        const loginResponse = await axios.post(`${API_BASE_URL}/auth/login/`, {
          username: 'testuser_integration',
          password: 'testpass123'
        })
        authToken = loginResponse.data.access
      } catch (loginError) {
        console.error('Failed to authenticate:', loginError)
      }
    }
  })

  describe('Authentication API', () => {
    it('should register a new user', async () => {
      const response = await axios.post(`${API_BASE_URL}/auth/register/`, {
        username: `testuser_${Date.now()}`,
        email: `test_${Date.now()}@example.com`,
        password: 'testpass123',
        password2: 'testpass123'
      })
      expect(response.status).toBe(201)
      expect(response.data).toHaveProperty('access')
      expect(response.data).toHaveProperty('refresh')
      expect(response.data).toHaveProperty('user')
    })

    it('should login with valid credentials', async () => {
      const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
        username: 'testuser_integration',
        password: 'testpass123'
      })
      expect(response.status).toBe(200)
      expect(response.data).toHaveProperty('access')
      expect(response.data).toHaveProperty('refresh')
    })

    it('should fail login with invalid credentials', async () => {
      try {
        await axios.post(`${API_BASE_URL}/auth/login/`, {
          username: 'testuser_integration',
          password: 'wrongpassword'
        })
        fail('Should have thrown an error')
      } catch (error: any) {
        expect(error.response.status).toBe(401)
      }
    })

    it('should get user profile when authenticated', async () => {
      if (!authToken) {
        return // Skip if no token
      }
      const response = await axios.get(`${API_BASE_URL}/auth/user/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      expect(response.status).toBe(200)
      expect(response.data).toHaveProperty('username')
    })
  })

  describe('Products API', () => {
    it('should fetch all products', async () => {
      const response = await axios.get(`${API_BASE_URL}/products/`)
      expect(response.status).toBe(200)
      expect(Array.isArray(response.data.results) || Array.isArray(response.data)).toBe(true)
    })

    it('should fetch featured products', async () => {
      const response = await axios.get(`${API_BASE_URL}/products/featured/`)
      expect(response.status).toBe(200)
      expect(Array.isArray(response.data)).toBe(true)
      expect(response.data.length).toBeLessThanOrEqual(8)
    })

    it('should search products', async () => {
      const response = await axios.get(`${API_BASE_URL}/products/?search=spotify`)
      expect(response.status).toBe(200)
      const products = response.data.results || response.data
      expect(Array.isArray(products)).toBe(true)
    })

    it('should fetch categories', async () => {
      const response = await axios.get(`${API_BASE_URL}/products/categories/`)
      expect(response.status).toBe(200)
      expect(Array.isArray(response.data.results) || Array.isArray(response.data)).toBe(true)
    })
  })

  describe('Orders API', () => {
    it('should create an order', async () => {
      const response = await axios.post(`${API_BASE_URL}/orders/`, {
        customer_name: 'Test Customer',
        customer_email: 'customer@example.com',
        items: [
          {
            product_name: 'Spotify Premium',
            product_price: '9.99',
            quantity: 1
          }
        ]
      })
      expect(response.status).toBe(201)
      expect(response.data).toHaveProperty('id')
      expect(response.data).toHaveProperty('total_amount')
      expect(response.data.items.length).toBe(1)
    })

    it('should fetch all orders', async () => {
      const response = await axios.get(`${API_BASE_URL}/orders/`)
      expect(response.status).toBe(200)
      expect(Array.isArray(response.data.results) || Array.isArray(response.data)).toBe(true)
    })
  })

  describe('Reviews API', () => {
    let productId: number
    let reviewId: number

    beforeAll(async () => {
      // Get a product ID for testing
      const productsResponse = await axios.get(`${API_BASE_URL}/products/`)
      const products = productsResponse.data.results || productsResponse.data
      if (products && products.length > 0) {
        productId = products[0].id
      }
    })

    it('should create a review when authenticated', async () => {
      if (!authToken || !productId) {
        return // Skip if no token or product
      }
      const response = await axios.post(
        `${API_BASE_URL}/reviews/`,
        {
          product: productId,
          rating: 5,
          title: 'Great product!',
          comment: 'Really enjoyed using this product.'
        },
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      )
      expect(response.status).toBe(201)
      expect(response.data).toHaveProperty('id')
      expect(response.data.rating).toBe(5)
      reviewId = response.data.id
    })

    it('should fail to create review when unauthenticated', async () => {
      if (!productId) {
        return // Skip if no product
      }
      try {
        await axios.post(`${API_BASE_URL}/reviews/`, {
          product: productId,
          rating: 5,
          title: 'Test',
          comment: 'Test comment'
        })
        fail('Should have thrown an error')
      } catch (error: any) {
        expect(error.response.status).toBe(401)
      }
    })

    it('should fetch product reviews', async () => {
      if (!productId) {
        return // Skip if no product
      }
      const response = await axios.get(
        `${API_BASE_URL}/reviews/product_reviews/?product_id=${productId}`
      )
      expect(response.status).toBe(200)
      expect(response.data).toHaveProperty('reviews')
      expect(response.data).toHaveProperty('average_rating')
      expect(response.data).toHaveProperty('total_reviews')
    })

    it('should fetch my reviews when authenticated', async () => {
      if (!authToken) {
        return // Skip if no token
      }
      const response = await axios.get(`${API_BASE_URL}/reviews/my_reviews/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      expect(response.status).toBe(200)
      expect(Array.isArray(response.data)).toBe(true)
    })

    it('should update a review when authenticated', async () => {
      if (!authToken || !reviewId || !productId) {
        return // Skip if missing requirements
      }
      const response = await axios.put(
        `${API_BASE_URL}/reviews/${reviewId}/`,
        {
          product: productId,
          rating: 4,
          title: 'Updated review',
          comment: 'Updated comment'
        },
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      )
      expect(response.status).toBe(200)
      expect(response.data.rating).toBe(4)
    })

    it('should delete a review when authenticated', async () => {
      if (!authToken || !reviewId) {
        return // Skip if missing requirements
      }
      const response = await axios.delete(`${API_BASE_URL}/reviews/${reviewId}/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      expect(response.status).toBe(204)
    })
  })

  describe('Full Workflow Tests', () => {
    it('should complete a full purchase workflow', async () => {
      // 1. Get products
      const productsResponse = await axios.get(`${API_BASE_URL}/products/`)
      const products = productsResponse.data.results || productsResponse.data
      expect(products.length).toBeGreaterThan(0)

      // 2. Create order
      const orderResponse = await axios.post(`${API_BASE_URL}/orders/`, {
        customer_name: 'Workflow Test Customer',
        customer_email: 'workflow@example.com',
        items: [
          {
            product_name: products[0].name,
            product_price: products[0].price,
            quantity: 1
          }
        ]
      })
      expect(orderResponse.status).toBe(201)
      expect(orderResponse.data.total_amount).toBe(products[0].price)
    })

    it('should complete a review workflow', async () => {
      if (!authToken) {
        return // Skip if no token
      }

      // 1. Get a product
      const productsResponse = await axios.get(`${API_BASE_URL}/products/`)
      const products = productsResponse.data.results || productsResponse.data
      if (!products || products.length === 0) {
        return // Skip if no products
      }
      const productId = products[0].id

      // 2. Create a review
      const reviewResponse = await axios.post(
        `${API_BASE_URL}/reviews/`,
        {
          product: productId,
          rating: 5,
          title: 'Workflow Test Review',
          comment: 'This is a test review from the workflow test.'
        },
        {
          headers: { Authorization: `Bearer ${authToken}` }
        }
      )
      expect(reviewResponse.status).toBe(201)

      // 3. Get product reviews
      const reviewsResponse = await axios.get(
        `${API_BASE_URL}/reviews/product_reviews/?product_id=${productId}`
      )
      expect(reviewsResponse.status).toBe(200)
      expect(reviewsResponse.data.total_reviews).toBeGreaterThan(0)
    })
  })
})

