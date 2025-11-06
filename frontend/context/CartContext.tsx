'use client'

import { createContext, useState, useEffect, ReactNode } from 'react'

export interface CartItem {
  product_name: string
  product_price: string
  quantity: number
}

interface CartContextType {
  cartItems: CartItem[]
  addToCart: (item: CartItem) => void
  removeFromCart: (index: number) => void
  updateQuantity: (index: number, quantity: number) => void
  clearCart: () => void
}

export const CartContext = createContext<CartContextType>({
  cartItems: [],
  addToCart: () => {},
  removeFromCart: () => {},
  updateQuantity: () => {},
  clearCart: () => {},
})

export function CartProvider({ children }: { children: ReactNode }) {
  const [cartItems, setCartItems] = useState<CartItem[]>([])

  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      setCartItems(JSON.parse(savedCart))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cartItems))
  }, [cartItems])

  const addToCart = (item: CartItem) => {
    setCartItems((prev) => {
      const existingIndex = prev.findIndex(
        (i) => i.product_name === item.product_name
      )
      if (existingIndex >= 0) {
        const updated = [...prev]
        updated[existingIndex].quantity += item.quantity
        return updated
      }
      return [...prev, item]
    })
  }

  const removeFromCart = (index: number) => {
    setCartItems((prev) => prev.filter((_, i) => i !== index))
  }

  const updateQuantity = (index: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(index)
      return
    }
    setCartItems((prev) => {
      const updated = [...prev]
      updated[index].quantity = quantity
      return updated
    })
  }

  const clearCart = () => {
    setCartItems([])
  }

  return (
    <CartContext.Provider
      value={{
        cartItems,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

