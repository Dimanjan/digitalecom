'use client'

import { useContext } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { CartContext } from '@/context/CartContext'
import { Product } from '@/types'
import { FiShoppingCart } from 'react-icons/fi'

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addToCart } = useContext(CartContext)

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault()
    addToCart({
      product_name: product.name,
      product_price: product.price.toString(),
      quantity: 1,
    })
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <Link href={`/products/${product.slug}`}>
        <div className="relative h-48 bg-gradient-to-br from-primary-100 to-primary-200">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-primary-600 text-4xl font-bold">
              {product.name.charAt(0)}
            </div>
          )}
        </div>
      </Link>
      <div className="p-6">
        <Link href={`/products/${product.slug}`}>
          <h3 className="text-xl font-semibold text-gray-900 mb-2 hover:text-primary-600 transition-colors">
            {product.name}
          </h3>
        </Link>
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {product.description}
        </p>
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-primary-600">
            ${parseFloat(product.price).toFixed(2)}
          </span>
          <button
            onClick={handleAddToCart}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
          >
            <FiShoppingCart className="w-4 h-4" />
            <span>Add to Cart</span>
          </button>
        </div>
        {product.category && (
          <div className="mt-3">
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {product.category.name}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}

