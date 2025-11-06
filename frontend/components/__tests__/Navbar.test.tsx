import { render, screen } from '@testing-library/react'
import Navbar from '../Navbar'
import { CartProvider } from '@/context/CartContext'

describe('Navbar', () => {
  it('renders navigation links', () => {
    render(
      <CartProvider>
        <Navbar />
      </CartProvider>
    )

    expect(screen.getByText('DigitalStore')).toBeInTheDocument()
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('Products')).toBeInTheDocument()
  })

  it('renders cart icon', () => {
    render(
      <CartProvider>
        <Navbar />
      </CartProvider>
    )

    // Cart icon should be present
    const cartLink = screen.getByRole('link', { name: /cart/i })
    expect(cartLink).toBeInTheDocument()
  })
})

