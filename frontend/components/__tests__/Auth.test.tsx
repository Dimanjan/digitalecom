import { render, screen } from '@testing-library/react'
import { useContext } from 'react'
import { AuthContext, AuthProvider } from '@/context/AuthContext'

describe('AuthContext', () => {
  it('provides authentication state', () => {
    const TestComponent = () => {
      const { isAuthenticated, user } = useContext(AuthContext)
      return (
        <div>
          {isAuthenticated ? `Logged in as ${user?.username}` : 'Not logged in'}
        </div>
      )
    }

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    // Initially not authenticated
    expect(screen.getByText('Not logged in')).toBeInTheDocument()
  })
})

