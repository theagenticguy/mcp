# Routing Implementation with React Router and Amplify Auth

This guide shows how to implement authenticated and unauthenticated routes using React Router v7 and Amplify Authentication.

## Basic Router Setup

```tsx
// src/App.tsx
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from 'react-router';
import { Authenticator } from '@aws-amplify/ui-react';
import { useAuth } from './hooks/useAuth';

// Protected Route Component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// Public Route Component
const PublicRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

// Layout Components
const AuthenticatedLayout = () => (
  <div className="min-h-screen bg-background">
    <Navbar />
    <main className="container mx-auto px-4 py-8">
      <Outlet />
    </main>
  </div>
);

const PublicLayout = () => (
  <div className="min-h-screen bg-background">
    <main>
      <Outlet />
    </main>
  </div>
);

// Route Configuration
const router = createBrowserRouter([
  {
    path: "/",
    element: <PublicLayout />,
    children: [
      {
        index: true,
        element: (
          <PublicRoute>
            <LandingPage />
          </PublicRoute>
        ),
      },
      {
        path: "login",
        element: (
          <PublicRoute>
            <Authenticator />
          </PublicRoute>
        ),
      },
      {
        path: "signup",
        element: (
          <PublicRoute>
            <Authenticator initialState="signUp" />
          </PublicRoute>
        ),
      },
    ],
  },
  {
    path: "/dashboard",
    element: <AuthenticatedLayout />,
    children: [
      {
        index: true,
        element: (
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        ),
      },
      {
        path: "profile",
        element: (
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        ),
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/" replace />,
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
```

## Authentication Hook

```tsx
// src/hooks/useAuth.ts
import { useEffect, useState } from 'react';
import { Auth } from 'aws-amplify';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      await Auth.currentAuthenticatedUser();
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  }

  return { isAuthenticated, isLoading };
}
```

## Best Practices

1. **Route Organization**
   - Use `createBrowserRouter` for type-safe route configuration
   - Group routes by authentication status and layout
   - Implement nested routes for better organization
   - Use layout components for consistent UI

2. **Authentication Flow**
   - Handle loading states
   - Implement proper error handling
   - Use protected routes for sensitive data
   - Leverage React Router's built-in navigation

3. **Navigation**
   - Use `Navigate` for programmatic navigation
   - Implement proper redirects after auth state changes
   - Handle 404 routes gracefully
   - Use relative paths in nested routes

4. **Security**
   - Always verify authentication on protected routes
   - Implement proper session management
   - Use secure routing patterns
   - Leverage React Router's built-in protection

## Example Usage

```tsx
// Example of a protected dashboard page
import { AuthenticatedLayout } from '../components/layout/AuthenticatedLayout';

export function Dashboard() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {/* Dashboard content */}
    </div>
  );
}
``` 