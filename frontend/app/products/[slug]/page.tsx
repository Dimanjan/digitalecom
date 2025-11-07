'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Image from 'next/image'
import { useContext } from 'react'
import { CartContext } from '@/context/CartContext'
import { Product } from '@/types'
import { getProducts } from '@/lib/api'
import { FiShoppingCart } from 'react-icons/fi'
import ReviewList from '@/components/ReviewList'
import ReviewForm from '@/components/ReviewForm'

export default function ProductDetailPage() {
  const params = useParams()
  const slug = params?.slug as string
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [reviewKey, setReviewKey] = useState(0)
  const { addToCart } = useContext(CartContext)

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const products = await getProducts()
        const foundProduct = products.find((p) => p.slug === slug)
        if (foundProduct) {
          setProduct(foundProduct)
        } else {
          setProduct(null)
        }
      } catch (error) {
        console.error('Error fetching product:', error)
        setProduct(null)
      } finally {
        setLoading(false)
      }
    }
    if (slug) {
      fetchProduct()
    }
  }, [slug])

  const handleAddToCart = () => {
    if (product) {
      addToCart({
        product_name: product.name,
        product_price: product.price,
        quantity: 1,
      })
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Product not found</h1>
        <p className="text-gray-600">The product you're looking for doesn't exist.</p>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="relative h-96 bg-gradient-to-br from-primary-100 to-primary-200">
            {product.image_url ? (
              <Image
                src={product.image_url}
                alt={product.name}
                fill
                className="object-cover"
              />
            ) : (
              <div className="flex items-center justify-center h-full text-primary-600 text-6xl font-bold">
                {product.name.charAt(0)}
              </div>
            )}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{product.name}</h1>
          {product.category && (
            <span className="inline-block text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded mb-4">
              {product.category.name}
            </span>
          )}
          <p className="text-3xl font-bold text-primary-600 mb-6">
            ${parseFloat(product.price).toFixed(2)}
          </p>
          <p className="text-gray-700 mb-6 leading-relaxed">{product.description}</p>
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-gray-600">
              <span className="font-semibold">Stock:</span>
              <span>{product.stock > 0 ? `${product.stock} available` : 'Out of stock'}</span>
            </div>
            <button
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              className="w-full bg-primary-600 text-white py-4 rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              <FiShoppingCart className="w-5 h-5" />
              <span>Add to Cart</span>
            </button>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <ReviewList key={reviewKey} productId={product.id} />
        <ReviewForm 
          productId={product.id} 
          onReviewSubmitted={() => setReviewKey(prev => prev + 1)} 
        />
      </div>
    </div>
  )
}

