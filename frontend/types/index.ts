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

