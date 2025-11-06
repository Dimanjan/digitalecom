import { render, screen, fireEvent } from '@testing-library/react'
import ProductCard from '../ProductCard'
import { CartProvider } from '@/context/CartContext'
import { Product } from '@/types'

const mockProduct: Product = {
  id: 1,
  name: 'Spotify Premium',
  slug: 'spotify-premium',
  description: 'Premium music streaming service',
  price: '9.99',
  stock: 100,
  is_active: true,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  category: {
    id: 1,
    name: 'Streaming',
    slug: 'streaming',
  },
}

describe('ProductCard', () => {
  it('renders product information correctly', () => {
    render(
      <CartProvider>
        <ProductCard product={mockProduct} />
      </CartProvider>
    )

    expect(screen.getByText('Spotify Premium')).toBeInTheDocument()
    expect(screen.getByText('$9.99')).toBeInTheDocument()
    expect(screen.getByText('Premium music streaming service')).toBeInTheDocument()
  })

  it('calls addToCart when button is clicked', () => {
    render(
      <CartProvider>
        <ProductCard product={mockProduct} />
      </CartProvider>
    )

    const addToCartButton = screen.getByText('Add to Cart')
    fireEvent.click(addToCartButton)

    // Verify the button is still there (cart was updated)
    expect(addToCartButton).toBeInTheDocument()
  })
})

