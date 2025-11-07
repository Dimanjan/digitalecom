import { render, screen, waitFor } from '@testing-library/react'
import ReviewList from '../ReviewList'
import { getProductReviews } from '@/lib/api'

jest.mock('@/lib/api')

const mockReviews = {
  reviews: [
    {
      id: 1,
      product: 1,
      user: {
        id: 1,
        username: 'testuser',
        first_name: 'Test',
        last_name: 'User',
      },
      rating: 5,
      title: 'Great product!',
      comment: 'Really enjoyed using this.',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
  ],
  average_rating: 5.0,
  total_reviews: 1,
}

describe('ReviewList', () => {
  beforeEach(() => {
    (getProductReviews as jest.Mock).mockResolvedValue(mockReviews)
  })

  it('renders reviews correctly', async () => {
    render(<ReviewList productId={1} />)
    
    await waitFor(() => {
      expect(screen.getByText('Great product!')).toBeInTheDocument()
      expect(screen.getByText('by testuser')).toBeInTheDocument()
    })
  })

  it('displays average rating', async () => {
    render(<ReviewList productId={1} />)
    
    await waitFor(() => {
      expect(screen.getByText('5.0 out of 5')).toBeInTheDocument()
      expect(screen.getByText('(1 review)')).toBeInTheDocument()
    })
  })

  it('shows message when no reviews', async () => {
    (getProductReviews as jest.Mock).mockResolvedValue({
      reviews: [],
      average_rating: 0,
      total_reviews: 0,
    })
    
    render(<ReviewList productId={1} />)
    
    await waitFor(() => {
      expect(screen.getByText(/No reviews yet/)).toBeInTheDocument()
    })
  })
})

