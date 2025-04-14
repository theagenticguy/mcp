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
npx shadcn@latest init
```

During the initialization process, for the color base, select "Neutral".

Now you can install shadcn/ui components as needed. The following components are used for most types of applications and should be installed. Others can be installed as needed.

If prompted, choose the --force flag to avoid dependency issues as these are new versions of the packages. 

```bash
npx shadcn add select card dialog textarea badge label form table collapsible avatar dropdown-menu skeleton input tooltip sheet button separator breadcrumb sidebar
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
│   │   └── app-sidebar.tsx            # main application sidebar with logo, menu, user
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

## create the src/components/app-sidebar.tsx 

```tsx
import type * as React from "react"
import {
  BadgeCheck,
  Bell,
  BookOpen,
  Bot,
  ChevronRight,
  ChevronsUpDown,
  CreditCard,
  GalleryVerticalEnd,
  LogOut,
  Settings2,
  Sparkles,
  SquareTerminal,
} from "lucide-react"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
  useSidebar,
} from "@/components/ui/sidebar"

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Playground",
      url: "#",
      icon: SquareTerminal,
      isActive: true,
      items: [
        {
          title: "History",
          url: "#",
        },
        {
          title: "Starred",
          url: "#",
        },
        {
          title: "Settings",
          url: "#",
        },
      ],
    },
    {
      title: "Models",
      url: "#",
      icon: Bot,
      items: [
        {
          title: "Genesis",
          url: "#",
        },
        {
          title: "Explorer",
          url: "#",
        },
        {
          title: "Quantum",
          url: "#",
        },
      ],
    },
    {
      title: "Documentation",
      url: "#",
      icon: BookOpen,
      items: [
        {
          title: "Introduction",
          url: "#",
        },
        {
          title: "Get Started",
          url: "#",
        },
        {
          title: "Tutorials",
          url: "#",
        },
        {
          title: "Changelog",
          url: "#",
        },
      ],
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings2,
      items: [
        {
          title: "General",
          url: "#",
        },
        {
          title: "Team",
          url: "#",
        },
        {
          title: "Billing",
          url: "#",
        },
        {
          title: "Limits",
          url: "#",
        },
      ],
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { isMobile } = useSidebar()

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg">
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <GalleryVerticalEnd className="size-4" />
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold">Dashboard</span>
                <span className="text-xs">v1.0.0</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {data.navMain.map((item) => (
              <Collapsible key={item.title} asChild defaultOpen={item.isActive} className="group/collapsible">
                <SidebarMenuItem>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton tooltip={item.title}>
                      {item.icon && <item.icon />}
                      <span>{item.title}</span>
                      <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {item.items?.map((subItem) => (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton asChild>
                            <a href={subItem.url}>
                              <span>{subItem.title}</span>
                            </a>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      ))}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </SidebarMenuItem>
              </Collapsible>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton
                  size="lg"
                  className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                >
                  <Avatar className="h-8 w-8 rounded-lg">
                    <AvatarImage src={data.user.avatar || "/placeholder.svg"} alt={data.user.name} />
                    <AvatarFallback className="rounded-lg">CN</AvatarFallback>
                  </Avatar>
                  <div className="grid flex-1 text-left text-sm leading-tight">
                    <span className="truncate font-semibold">{data.user.name}</span>
                    <span className="truncate text-xs">{data.user.email}</span>
                  </div>
                  <ChevronsUpDown className="ml-auto size-4" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                side={isMobile ? "bottom" : "right"}
                align="end"
                sideOffset={4}
              >
                <DropdownMenuLabel className="p-0 font-normal">
                  <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                    <Avatar className="h-8 w-8 rounded-lg">
                      <AvatarImage src={data.user.avatar || "/placeholder.svg"} alt={data.user.name} />
                      <AvatarFallback className="rounded-lg">CN</AvatarFallback>
                    </Avatar>
                    <div className="grid flex-1 text-left text-sm leading-tight">
                      <span className="truncate font-semibold">{data.user.name}</span>
                      <span className="truncate text-xs">{data.user.email}</span>
                    </div>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Upgrade to Pro
                  </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem>
                    <BadgeCheck className="mr-2 h-4 w-4" />
                    Account
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <CreditCard className="mr-2 h-4 w-4" />
                    Billing
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Bell className="mr-2 h-4 w-4" />
                    Notifications
                  </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <LogOut className="mr-2 h-4 w-4" />
                  Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}

```

