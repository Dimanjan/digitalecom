import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ReviewForm from '../ReviewForm'
import { AuthContext } from '@/context/AuthContext'
import { createReview } from '@/lib/api'

jest.mock('@/lib/api')

const mockAuthContext = {
  user: { id: 1, username: 'testuser' },
  loading: false,
  login: jest.fn(),
  register: jest.fn(),
  logout: jest.fn(),
  isAuthenticated: true,
}

describe('ReviewForm', () => {
  beforeEach(() => {
    (createReview as jest.Mock).mockResolvedValue({ id: 1 })
  })

  it('renders form when authenticated', () => {
    render(
      <AuthContext.Provider value={mockAuthContext as any}>
        <ReviewForm productId={1} />
      </AuthContext.Provider>
    )

    expect(screen.getByText('Write a Review')).toBeInTheDocument()
    expect(screen.getByLabelText(/Review Title/)).toBeInTheDocument()
    expect(screen.getByLabelText(/Your Review/)).toBeInTheDocument()
  })

  it('shows login message when not authenticated', () => {
    const unauthenticatedContext = {
      ...mockAuthContext,
      isAuthenticated: false,
    }

    render(
      <AuthContext.Provider value={unauthenticatedContext as any}>
        <ReviewForm productId={1} />
      </AuthContext.Provider>
    )

    expect(screen.getByText(/Please login/)).toBeInTheDocument()
  })

  it('submits review on form submit', async () => {
    const onReviewSubmitted = jest.fn()

    render(
      <AuthContext.Provider value={mockAuthContext as any}>
        <ReviewForm productId={1} onReviewSubmitted={onReviewSubmitted} />
      </AuthContext.Provider>
    )

    fireEvent.change(screen.getByLabelText(/Review Title/), {
      target: { value: 'Great product!' },
    })
    fireEvent.change(screen.getByLabelText(/Your Review/), {
      target: { value: 'Really enjoyed this.' },
    })
    fireEvent.click(screen.getByText('Submit Review'))

    await waitFor(() => {
      expect(createReview).toHaveBeenCalledWith({
        product: 1,
        rating: 5,
        title: 'Great product!',
        comment: 'Really enjoyed this.',
      })
    })
  })
})

