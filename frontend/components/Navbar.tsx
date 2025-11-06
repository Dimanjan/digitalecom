'use client'

import Link from 'next/link'
import { useContext } from 'react'
import { CartContext } from '@/context/CartContext'
import { FiShoppingCart } from 'react-icons/fi'

export default function Navbar() {
  const { cartItems } = useContext(CartContext)
  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-2xl font-bold text-primary-600">
            DigitalStore
          </Link>
          <div className="flex items-center gap-6">
            <Link
              href="/"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              Home
            </Link>
            <Link
              href="/products"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              Products
            </Link>
            <Link
              href="/cart"
              className="relative text-gray-700 hover:text-primary-600 transition-colors"
            >
              <FiShoppingCart className="w-6 h-6" />
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-primary-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

