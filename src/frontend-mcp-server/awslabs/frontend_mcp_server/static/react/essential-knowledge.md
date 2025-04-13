The following steps should be followed in sequence to create a new web application on AWS

Follow the instructions in "basic-ui-setup" topic to setup the base application using the following stack. These are very new libraries and the exact instructions and commands should be used.
- React 19 with TypeScript using Vite
- Tailwind 4 for styling
- shadcn for UI components
- AWS Amplify Gen 2 library for authentication

Follow the instructions in "authentication-setup" to setup authentication against the pre-existing cognito backend using the Amplify Authenticator UI component and hooks

Follow the instructions in "routing-setup" to setup routing for key pages in the application

Follow the instructions in "creating-components" when new components need to be created or added. shadcn should be your first choice for components vs. creating new components

Follow the instructions in "customizing-the-application" to customize the application based on the functional needs of the application

General guidelines:
- Install and use shadcn components where available vs. creating custom components
- For simplicity and maintainability, prefer using Zustand stores for global state management vs. component level state/prop-drilling
- Create an application name, descriptio, and sample data based on the functional purpose of the application to make it more realistic

