# Amplify Authentication Setup Guide

Here's how to setup authentication for a web application with AWS Amplify Authenticator UI component and hooks

## Instructions

Install @aws-amplify/ui-react and aws-amplify 

Configure Amplify in main.tsx

Using shadcn components, create the layout for unauthenticated pages in src/layouts/UnauthenticatedLayout.tsx as follows
1. The page should be a 50/50 split with the left side an image placeholder with application name and description in bottom left with ample margin
2. The right side should have the Amplify Authenticator component v/h centered

Using shadcn components, create a src/pages/Login.tsx page that uses UnauthenticatedLayout.tsx

Using shadcn components, create the layout for authenticated pages in src/layout/AuthenticatedLayout.tsx as follows. Update or create the src/components/app-sidebar.tsx
1. The layout should have left sidebar that has the brand logo and application name on the left. The user name and avatar on the bottom of the sidebar, with dropdown to a Signout option
2. Links to the main pages
3. A main content area that holds the current page based on the route

Create the necessary authenticated and unauthenticated routes

Wire up the functionality to ensure that authenticated pages are only accessible after the user signs in. Use the zustand store to track user and login state.

## Code Snippets for Reference

### Main Configuration
```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Authenticator } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import App from './App.tsx';
import outputs from '../amplify_outputs.json';
import './index.css';
import '@aws-amplify/ui-react/styles.css';

Amplify.configure(outputs);
```

### Authenticator UI Component
```tsx
import React from 'react';
import { Amplify } from 'aws-amplify';

import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

export default function TestPage() {
  return (
    <Authenticator>
      {({ signOut, user }) => (
        <main>
          <h1>Hello {user.username}</h1>
          <button onClick={signOut}>Sign out</button>
        </main>
      )}
    </Authenticator>
  );
}
```

### Sign Out Implementation
```tsx
import { useAuthenticator } from '@aws-amplify/ui-react';

function App() {
  const { signOut } = useAuthenticator();

  return (
    <main>
      <button onClick={signOut}>Sign out</button>
    </main>
  );
}
```

### User Information Access
```tsx
import { useAuthenticator } from '@aws-amplify/ui-react';

function Component() {
  const { user } = useAuthenticator();
  return <p>Welcome, {user?.attributes?.email}</p>;
}
```
