# Setting Up a React 19 Project with Tailwind 4 and shadcn/ui

Here is how to create a modern web application with React 19 project with Tailwind CSS 4 and shadcn/ui components. It uses AWS Amplify v6 Gen 2 library to connect the frontend to the pre-existing AWS cloud backend. Use react-router v7 for routing. Use zustand for centralized state management. Use lucide-react for icons.

## Things you MUST remember as these are common mistakes

- React 19 and Tailwind 4 are very very new, you must refer to this documentation to get the installation right.
- Tailwind 4 has a new installation method and dependencies, follow the instructions in this guide to install it
- The shadcn package name is shadcn and not shadcn-ui
- When adding new shadcn components, select the force option if prompted, to avoid dependency issues. If a component already exists, choose not to overwrite it.
- Always prefer using official shadcn components when building the UI vs. creating custom components from scratch
- Always use Amplify v6 Gen 2 as that is the latest version
- Use the Authenticator component and hooks from Amplify instead of writing custom authentication UI components and logic
- Amplify MUST not be used for creating the backend or hosting the web application. Those will be handled by CDK and other parts of the solution. Amplify should only used to simplify how the React web app talks to the pre-existing AWS backend. 
- Ensure you follow the instructions in this guide exactly and in the order provided

## Create a New React Project

```bash
npm create vite@latest my-react-app -- --template react-ts
cd my-react-app
```

## Add Tailwind CSS 4

Install Tailwind 4 CSS and its Vite plugin:

```bash
npm install tailwindcss @tailwindcss/vite
```

Replace everything in `src/index.css` with the following:

```css
@import "tailwindcss";
```

### Configure TypeScript

Update your `tsconfig.json` file to add path aliases:

```json
{
  "files": [],
  "references": [
    {
      "path": "./tsconfig.app.json"
    },
    {
      "path": "./tsconfig.node.json"
    }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Then update your `tsconfig.app.json` file:

```json
{
  "compilerOptions": {
    // ...
    "baseUrl": ".",
    "paths": {
      "@/*": [
        "./src/*"
      ]
    }
    // ...
  }
}
```

### Update Vite Configuration

Install the required dev dependency:

```bash
npm install -D @types/node
```

Update your `vite.config.ts` file:

```typescript
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
 
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

## Install and Configure shadcn/ui

IMPORTANT: You must verify that Tailwind 4 (not a previous version) was installed following the steps above before proceeding further. Validate that all the files above have been updated correctly. Do not install an older version of Tailwind (e.g. versions that do not have vite integration or use autoprefixer) as that will prevent the application from working.

Run the shadcn CLI to set up your project:

```bash
npx shadcn@latest init -s
```

During the initialization process, for the color base, select "Neutral".

Now you can install shadcn/ui components as needed. You must use the --force flag to avoid dependency issues

```bash
npx shadcn@latest add button -s
```

## Install other required libraries

```bash
npm install react-router zustand lucide-react
```

## Install AWS Amplify Gen 2

We will use Amplify Gen2 to connect the UI to the AWS backend that has already been created. To add AWS Amplify Gen 2 to your project, install the required dependencies:

```bash
npm install @aws-amplify/ui-react aws-amplify
```

This will allow you to use Amplify UI components and the Amplify JavaScript libraries to interact with your AWS backend resources.


## Project Structure

After setup, your project structure should look similar to this. This example is for a task tracking app.

```
my-task-app/
├── public/                            # Static assets
│   └── favicon.ico
│   └── login-splash.png               # splash image for login screen 
├── src/                               
│   ├── components/                    
│   │   └── ui/                        # shadcn/ui components
│   │       ├── button.tsx
|   |       └── ...
│   ├── features/                      # Feature-specific components and logic
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskDetailPage.tsx
│   │   │   ├── NewTaskPage.tsx
│   │   │   └── store.ts               # Zustand slice for tasks
│   │   └── users/
│   │       ├── UserManagementPage.tsx
│   │       └── store.ts               # Zustand slice for users
│   ├── layouts/                       # Layout components
│   │   ├── UnauthenticatedLayout.tsx  # Layout for unauthenticated pages
│   │   └── AuthenticatedLayout.tsx    # Layout for authenticated pages
│   ├── pages/                         
│   │   ├── Login.tsx                  # Login page using UnauthenticatedLayout.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ReportsPage.tsx
│   │   └── SettingsPage.tsx
│   ├── store/                         
│   │   └── index.ts                   # Main store combining feature slices
│   ├── App.tsx                        
│   ├── index.css                      
│   ├── main.tsx                       # Entry point with Amplify configuration
│   └── routes.tsx                     # route definition
├── index.html         
├── amplify_outputs.json               # Amplify configuration file
├── package.json                       
├── tailwind.config.ts             
├── tsconfig.json                    
└── vite.config.ts                 

```



