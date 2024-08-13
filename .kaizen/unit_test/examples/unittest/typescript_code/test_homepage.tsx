// examples/unittest/typescript_code/home.page.test.tsx

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import HomePage from './home.page';
import userEvent from '@testing-library/user-event';

// Mocking the user context
const mockUserContext = (user: any) => {
  jest.resetModules(); // Reset modules to ensure the mock is reset between tests
  jest.mock('./UserContext', () => ({
    useUser: () => ({
      user,
    }),
  }));
};

describe('HomePage Component', () => {
  afterEach(() => {
    jest.resetAllMocks();
  });

  test('renders HomePage component correctly', () => {
    mockUserContext(null);
    render(<HomePage />);
    expect(screen.getByText('Welcome to HomePage')).toBeInTheDocument();
  });

  test('displays user information when user is logged in', () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    mockUserContext(user);
    render(<HomePage />);
    expect(screen.getByText(`Welcome, ${user.name}`)).toBeInTheDocument();
    expect(screen.getByText(user.email)).toBeInTheDocument();
  });

  test('shows default content when no user is logged in', () => {
    mockUserContext(null);
    render(<HomePage />);
    expect(screen.getByText('Welcome to HomePage')).toBeInTheDocument();
  });

  test('handles case when user object has missing properties', () => {
    const user = { name: 'John Doe' }; // missing email
    mockUserContext(user);
    render(<HomePage />);
    expect(screen.getByText(`Welcome, ${user.name}`)).toBeInTheDocument();
    expect(screen.queryByText('john@example.com')).not.toBeInTheDocument();
  });

  test('handles errors during data fetching', async () => {
    jest.resetModules(); // Ensure the mock is reset
    jest.mock('./UserContext', () => ({
      useUser: () => {
        throw new Error('Failed to fetch user data');
      },
    }));
    render(<HomePage />);
    expect(screen.getByText('Error loading user data')).toBeInTheDocument();
  });
});