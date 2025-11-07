export interface Category {
  id: number
  name: string
  slug: string
  description?: string
}

export interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  image?: string
  image_url?: string | null
  category?: Category
  stock: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface OrderItem {
  id: number
  product_name: string
  product_price: string
  quantity: number
  subtotal: string
}

export interface Order {
  id: number
  customer_name: string
  customer_email: string
  total_amount: string
  status: string
  items: OrderItem[]
  created_at: string
  updated_at: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  date_joined: string
}

export interface AuthResponse {
  user: User
  access: string
  refresh: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password2: string
  first_name?: string
  last_name?: string
}

export interface Review {
  id: number
  product: number
  product_name?: string
  user: {
    id: number
    username: string
    first_name: string
    last_name: string
  }
  rating: number
  title: string
  comment: string
  created_at: string
  updated_at: string
}

export interface ReviewCreateData {
  product: number
  rating: number
  title: string
  comment: string
}

export interface ProductReviewsResponse {
  reviews: Review[]
  average_rating: number
  total_reviews: number
}

