'use client'

import { useEffect, useState } from 'react'
import { Review, ProductReviewsResponse } from '@/types'
import { getProductReviews } from '@/lib/api'
import { FiStar } from 'react-icons/fi'

interface ReviewListProps {
  productId: number
}

export default function ReviewList({ productId }: ReviewListProps) {
  const [reviewsData, setReviewsData] = useState<ProductReviewsResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const data = await getProductReviews(productId)
        setReviewsData(data)
      } catch (error) {
        console.error('Error fetching reviews:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchReviews()
  }, [productId])

  if (loading) {
    return <div className="text-center py-4">Loading reviews...</div>
  }

  if (!reviewsData || reviewsData.reviews.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No reviews yet. Be the first to review this product!</p>
      </div>
    )
  }

  return (
    <div className="mt-8">
      <div className="mb-6">
        <h3 className="text-2xl font-semibold text-gray-900 mb-2">Customer Reviews</h3>
        <div className="flex items-center gap-4">
          <div className="flex items-center">
            {[1, 2, 3, 4, 5].map((star) => (
              <FiStar
                key={star}
                className={`w-5 h-5 ${
                  star <= Math.round(reviewsData.average_rating)
                    ? 'fill-yellow-400 text-yellow-400'
                    : 'text-gray-300'
                }`}
              />
            ))}
          </div>
          <span className="text-lg font-medium text-gray-700">
            {reviewsData.average_rating.toFixed(1)} out of 5
          </span>
          <span className="text-gray-500">
            ({reviewsData.total_reviews} {reviewsData.total_reviews === 1 ? 'review' : 'reviews'})
          </span>
        </div>
      </div>

      <div className="space-y-6">
        {reviewsData.reviews.map((review) => (
          <div key={review.id} className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="font-semibold text-gray-900">{review.title}</h4>
                <p className="text-sm text-gray-600">
                  by {review.user.username} • {new Date(review.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="flex items-center">
                {[1, 2, 3, 4, 5].map((star) => (
                  <FiStar
                    key={star}
                    className={`w-4 h-4 ${
                      star <= review.rating
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-gray-300'
                    }`}
                  />
                ))}
              </div>
            </div>
            <p className="text-gray-700">{review.comment}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

