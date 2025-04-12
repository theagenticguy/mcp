# React Router v7 with TypeScript

This guide covers how to use React Router v7 with a folder framework approach, implementing protected routes with authentication, and using Zustand for state management.

## Introduction to React Router v7

React Router v7 is a major update that can function as both a library and a framework. This dual capability allows you to:

- Use it as a traditional routing library for client-side applications
- Leverage framework features like server-side rendering, code splitting, and file-based routing

The biggest change in v7 is the unified package structure - all functionality is now consolidated in a single `react-router` package.

## Installation

```bash
npm install react-router
# or
yarn add react-router
```

## Folder Framework Approach

React Router v7 introduces a folder-based routing approach similar to Next.js or Remix. This approach uses a routes configuration file and a directory structure that maps to your routes.

### Setting Up the Project Structure

```bash
project/
├── react-router.config.ts    # Router configuration
├── src/
│   ├── root.tsx              # Root component (entry point)
│   ├── entry.client.tsx      # Client entry
│   ├── routes/
│   │   ├── _layout.tsx       # Root layout
│   │   ├── index.tsx         # Home page (/)
│   │   ├── about.tsx         # About page (/about)
│   │   ├── dashboard/
│   │   │   ├── _layout.tsx   # Dashboard layout
│   │   │   ├── index.tsx     # Dashboard page (/dashboard)
│   │   │   ├── profile.tsx   # Profile page (/dashboard/profile)
│   │   │   └── settings.tsx  # Settings page (/dashboard/settings)
│   │   └── auth/
│   │       ├── login.tsx     # Login page (/auth/login)
│   │       └── register.tsx  # Register page (/auth/register)
│   └── lib/
│       ├── auth.ts           # Authentication utilities
│       └── store.ts          # Zustand store
└── tsconfig.json             # TypeScript configuration
```

### Configuration File

Create a `react-router.config.ts` file in your project root:

```typescript
import type { Config } from "react-router";

export default {
  appDirectory: "src",
  basename: "/",
  future: {
    v7_partialMatching: true,
    v7_relativeSplatPath: true,
  },
  routes: [
    // Optional explicit routes
  ],
} satisfies Config;
```

### Route Module Structure

Each route file can export specific functions and components that React Router will use:

```typescript
// src/routes/dashboard/profile.tsx
import { LoaderFunctionArgs, json } from "react-router";
import { useLoaderData } from "react-router";

// Data loader - runs before component renders
export async function loader({ params, request }: LoaderFunctionArgs) {
  // Fetch data for this route
  const userData = await fetchUserProfile();
  return json({ userData });
}

// Component that renders the route
export default function Profile() {
  // Type-safe access to loader data
  const { userData } = useLoaderData() as { userData: UserProfile };
  
  return (
    <div>
      <h1>User Profile</h1>
      <p>Name: {userData.name}</p>
      <p>Email: {userData.email}</p>
    </div>
  );
}

// Error boundary for this route
export function ErrorBoundary() {
  return <div>Something went wrong loading the profile!</div>;
}
```

### Layout Routes

Layout routes allow you to define shared UI elements around nested routes:

```typescript
// src/routes/_layout.tsx
import { Outlet } from "react-router";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function RootLayout() {
  return (
    <div className="app-container">
      <Navbar />
      <main className="content">
        <Outlet /> {/* Child routes will render here */}
      </main>
      <Footer />
    </div>
  );
}
```

## Authentication with Zustand

Zustand is a lightweight state management library that works well with React Router. Let's create a store for authentication:

### Authentication Store

```typescript
// src/lib/store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      
      login: async (email, password) => {
        set({ isLoading: true });
        try {
          // Call your API
          const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });
          
          const data = await response.json();
          
          if (!response.ok) throw new Error(data.message);
          
          set({ 
            token: data.token,
            user: data.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      logout: () => {
        set({ 
          token: null,
          user: null,
          isAuthenticated: false,
        });
      },
      
      checkAuth: async () => {
        const { token } = get();
        if (!token) return;
        
        set({ isLoading: true });
        try {
          // Verify token validity
          const response = await fetch('/api/me', {
            headers: { 
              'Authorization': `Bearer ${token}`,
            },
          });
          
          if (!response.ok) {
            // Token invalid
            set({ 
              token: null, 
              user: null, 
              isAuthenticated: false,
              isLoading: false,
            });
            return;
          }
          
          const data = await response.json();
          set({ 
            user: data.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },
    }),
    {
      name: 'auth-storage', // Local storage key
      partialize: (state) => ({ token: state.token }), // Only persist token
    },
  ),
);
```

## Protected Routes

We'll implement protected routes using loader functions and redirects:

### Route Protection with Loaders

```typescript
// src/lib/auth.ts
import { redirect } from "react-router";
import { useAuthStore } from "./store";

export function requireAuth(request: Request) {
  // Get auth state from zustand
  const { isAuthenticated, token } = useAuthStore.getState();
  
  // Get the URL the user is trying to access
  const url = new URL(request.url);
  const pathname = url.pathname;
  
  // If user is not authenticated, redirect to login with return URL
  if (!isAuthenticated || !token) {
    const params = new URLSearchParams();
    params.set("returnTo", pathname);
    return redirect(`/auth/login?${params.toString()}`);
  }
  
  // User is authenticated, allow access
  return null;
}
```

### Implementing the Protected Route Pattern

```typescript
// src/routes/dashboard/_layout.tsx
import { LoaderFunctionArgs, Outlet, redirect } from "react-router";
import { requireAuth } from "../../lib/auth";

export async function loader({ request }: LoaderFunctionArgs) {
  // Check auth and redirect if needed
  const authRedirect = requireAuth(request);
  if (authRedirect) return authRedirect;
  
  // Return data for the layout
  return { isAuthorized: true };
}

export default function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <nav className="dashboard-nav">
        <h2>Dashboard</h2>
        <ul>
          <li><a href="/dashboard">Overview</a></li>
          <li><a href="/dashboard/profile">Profile</a></li>
          <li><a href="/dashboard/settings">Settings</a></li>
        </ul>
      </nav>
      
      <div className="dashboard-content">
        <Outlet />
      </div>
    </div>
  );
}
```

### Dashboard Index Route

```typescript
// src/routes/dashboard/index.tsx
import { LoaderFunctionArgs, json } from "react-router";
import { useLoaderData } from "react-router";
import { requireAuth } from "../../lib/auth";

export async function loader({ request }: LoaderFunctionArgs) {
  // This redundancy ensures this route is still protected even if accessed directly
  const authRedirect = requireAuth(request);
  if (authRedirect) return authRedirect;
  
  // Fetch dashboard data
  const dashboardData = await fetchDashboardData();
  return json({ dashboardData });
}

export default function Dashboard() {
  const { dashboardData } = useLoaderData() as { dashboardData: any };
  
  return (
    <div>
      <h1>Dashboard</h1>
      <div className="dashboard-stats">
        {/* Display dashboard data here */}
      </div>
    </div>
  );
}
```

### Login Page with Return URL Support

```typescript
// src/routes/auth/login.tsx
import { Form, redirect, useNavigate, useSearchParams } from "react-router";
import { useState } from "react";
import { useAuthStore } from "../../lib/store";

export default function Login() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  
  // Get login function from Zustand store
  const login = useAuthStore(state => state.login);
  const isLoading = useAuthStore(state => state.isLoading);
  
  // Get return URL from query parameters
  const returnTo = searchParams.get("returnTo") || "/dashboard";
  
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    
    const formData = new FormData(event.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    
    try {
      await login(email, password);
      // Redirect to the return URL after successful login
      navigate(returnTo);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to login");
    }
  };
  
  return (
    <div className="login-page">
      <h1>Login</h1>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input 
            type="email"
            id="email"
            name="email"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input 
            type="password"
            id="password"
            name="password"
            required
          />
        </div>
        
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Logging in..." : "Login"}
        </button>
      </form>
      
      <p>
        Don't have an account? <a href="/auth/register">Register</a>
      </p>
    </div>
  );
}
```

### Initialize Auth State

We need to initialize auth state when the app loads:

```typescript
// src/root.tsx
import { useEffect } from "react";
import { Outlet } from "react-router";
import { useAuthStore } from "./lib/store";

export default function Root() {
  const checkAuth = useAuthStore(state => state.checkAuth);
  
  useEffect(() => {
    // Check auth status when app loads
    checkAuth();
  }, [checkAuth]);
  
  return <Outlet />;
}
```

## Initializing the Router

Finally, let's set up the application entry point:

```typescript
// src/entry.client.tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { HydratedRouter } from "react-router";

// Import your routes (generated by React Router's build process)
import { routes } from "./routes.generated";

const root = document.getElementById("root");

if (!root) {
  throw new Error("Root element not found!");
}

createRoot(root).render(
  <StrictMode>
    <HydratedRouter routes={routes} />
  </StrictMode>
);
```

## Conclusion

This guide demonstrates how to use React Router v7's folder framework approach with TypeScript, implementing protected routes with authentication redirection, and Zustand for state management. The combination of these technologies provides a type-safe, maintainable approach to building modern React applications.

Key takeaways:

1. React Router v7 simplifies the package structure and provides framework-like capabilities
2. The folder framework approach enables intuitive route organization
3. Zustand offers a lightweight and straightforward state management solution
4. Protected routes can be implemented using loaders and redirects
5. TypeScript integration provides type safety throughout the application

This approach scales well for larger applications while keeping the codebase organized and maintainable.
