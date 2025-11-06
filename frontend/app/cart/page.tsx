'use client'

import { useContext } from 'react'
import { CartContext } from '@/context/CartContext'
import { useRouter } from 'next/navigation'
import { FiShoppingCart, FiTrash2, FiPlus, FiMinus } from 'react-icons/fi'
import { createOrder } from '@/lib/api'

export default function CartPage() {
  const { cartItems, removeFromCart, updateQuantity, clearCart } = useContext(CartContext)
  const router = useRouter()

  const total = cartItems.reduce((sum, item) => sum + parseFloat(item.product_price) * item.quantity, 0)

  const handleCheckout = async () => {
    if (cartItems.length === 0) return

    const customerName = prompt('Enter your name:')
    const customerEmail = prompt('Enter your email:')

    if (!customerName || !customerEmail) {
      alert('Name and email are required')
      return
    }

    try {
      const orderData = {
        customer_name: customerName,
        customer_email: customerEmail,
        items: cartItems.map(item => ({
          product_name: item.product_name,
          product_price: item.product_price,
          quantity: item.quantity,
        })),
      }

      await createOrder(orderData)
      clearCart()
      alert('Order placed successfully!')
      router.push('/')
    } catch (error) {
      console.error('Error creating order:', error)
      alert('Failed to place order. Please try again.')
    }
  }

  if (cartItems.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <FiShoppingCart className="mx-auto text-6xl text-gray-300 mb-4" />
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Your cart is empty</h2>
          <p className="text-gray-600 mb-8">Add some products to get started!</p>
          <button
            onClick={() => router.push('/products')}
            className="bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
          >
            Browse Products
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            {cartItems.map((item, index) => (
              <div key={index} className="border-b border-gray-200 pb-6 mb-6 last:border-0 last:mb-0 last:pb-0">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{item.product_name}</h3>
                    <p className="text-2xl font-bold text-primary-600">${parseFloat(item.product_price).toFixed(2)}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQuantity(index, item.quantity - 1)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                        disabled={item.quantity <= 1}
                      >
                        <FiMinus className="w-4 h-4" />
                      </button>
                      <span className="text-lg font-medium w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(index, item.quantity + 1)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                      >
                        <FiPlus className="w-4 h-4" />
                      </button>
                    </div>
                    <button
                      onClick={() => removeFromCart(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <FiTrash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
                <div className="mt-4 text-right">
                  <p className="text-gray-600">
                    Subtotal: <span className="font-semibold text-gray-900">
                      ${(parseFloat(item.product_price) * item.quantity).toFixed(2)}
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Order Summary</h2>
            <div className="space-y-4 mb-6">
              <div className="flex justify-between text-gray-600">
                <span>Subtotal</span>
                <span>${total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>Tax</span>
                <span>$0.00</span>
              </div>
              <div className="border-t border-gray-200 pt-4">
                <div className="flex justify-between text-xl font-bold text-gray-900">
                  <span>Total</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>
            </div>
            <button
              onClick={handleCheckout}
              className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors mb-4"
            >
              Proceed to Checkout
            </button>
            <button
              onClick={clearCart}
              className="w-full bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
            >
              Clear Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

