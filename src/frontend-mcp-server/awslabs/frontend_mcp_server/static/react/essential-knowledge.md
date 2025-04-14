# Reference UI Application Development Guide

## Introduction
This document provides guidance for an LLM assistant helping users create custom web applications based on the reference UI template at https://github.com/sanjusunny/reference-ui. The template uses React, Tailwind CSS, React Router v7, shadcn UI components, AWS Amplify, and Zustand for state management. As the assisting LLM, you should use this information to analyze user requirements, suggest appropriate approaches, and provide implementation steps for customizing the reference template to meet their specific needs. Follow the structured approach outlined below to deliver high-quality applications efficiently while maintaining consistency with the existing architecture and best practices.

## Key Assumptions
- Authentication, basic routing, and private/public layouts are already implemented
- Sample dashboard and settings pages exist as reference
- AWS backend integration will be handled separately

## Project Implementation Flow

### 0. Requirements Analysis
- Generate a modern app name and description
- Identify the primary color for the app if provided by the user, if not use shadcn defaults (usually #171717)
- Identify target users and primary purpose
- List and prioritize core features
- Map features to existing template structure
- Identify new pages and components needed
- Reuse the current authentication layouts and flow
- Reuse the current private page layout, with the application sidebar on the left and page content on the right
- Always include a dashboard page as the start page, and incorporate charts and lists based on the functional needs of the application
- Incorporate an AI Chat assistant to the application if helpful
- Make the UI design contemporary, clean and minimal.

### 1. Document your plan

Once you have completed your analysis, you MUST create a CHECKLIST.md in the root folder of the project that documents that contains the following:
- Application name, description
- Application goals and core features
- A checklist listing the key pages that need to be created for this app. 

As you go through the instructions below, keep adding to and updating this checklist to ensure that you have completely created all the pages and features necessary to meet the functional needs of the application the user wants to create.

### 2. Setup & Configuration
```bash
# Clone repository to frontend folder
git clone https://github.com/sanjusunny/reference-ui.git frontend
cd frontend
npm install
```

Analyze this code base after cloning to understand how it is structured and the key architectural patterns and frontend stack.

Based on your analysis, update the README.md with an overview of the functional goal of the application and the frontend stack, including specific versions (e.g. React 18 instead of just React)

### 3. Application Branding
- Update package.json with new application name
- Update app name references in components (e.g., app-sidebar.tsx)
- Update the app name and description on the login page
- Update document title and metadata in index.html
- Customize the primary color for the application using Tailwind if the user has provided a custom primary color for the app
- When setting primary color, you MUST update both the Tailwind and Amplify theme to keep them in sync

### 4. Update Branding by Generating Images
- Use Nova Canvas MCP Server to create:
  - **favicon.png (320x320)**
    - Create a minimal abstract icon that represents the app concept
    - Use monochromatic shades of the primary color
    - Design should be simple enough to be recognizable at small sizes
    - Avoid text or complex details that won't scale down well
  - **splash.png (1024x1024)**
    - Create a more elaborate abstract design that extends the favicon concept
    - Use primarily dark shades of the primary color with subtle accent colors if appropriate
    - Design should convey the app's purpose through abstract visual elements
    - Can include subtle patterns, gradients, or geometric shapes
- Place both images in the /public folder using a cross-platform move command
- Replace existing app icon references with generated favicon.png

### 5. UI Development
- Add new pages following existing patterns
- Reuse existing pages, layouts, components where possible
- Install or use shadcn components vs. creating custom components where possible 
- Add required shadcn components: `npx shadcn add [component-name]`
- Keep component organization flat and simple
- Extend routing using react-router v7 as configured
- Update navigation components
- Add sample data to the Zustand store

### 6. Backend Configuration
- Create a mock `amplify_outputs.json` file for development
- Structure it to match expected backend resources
- This file will later be updated by an external build process

## Technical Guidelines

### State Management
- Always use central Zustand store instead of component state
- Avoid prop drilling completely
- Components should access store directly via hooks
- Only use component state for temporary UI states (form inputs while typing)

### Component Organization
- Keep component organization flat
- Place new components in appropriate existing folders
- Don't group by features unless app is complex
- Follow existing naming conventions
- Always use shadcn components if available

## Final check

Add these to the CHECKLIST.md and verify to make sure they are completed

- [ ] Generate modern app name/description
- [ ] Clone repo to "frontend" folder and install dependencies
- [ ] Update the README.md based on your analysis of the codebase and frontend stack
- [ ] Update package.json name and app name references
- [ ] Update app name and description on the login page
- [ ] Generate favicon.png and splash.png images
- [ ] Replace app icon references with generated favicon.png
- [ ] Create mock amplify_outputs.json file
- [ ] Add/update pages and required components, using shadcn components
- [ ] Extend routing structure
- [ ] Add sample data to Zustand store
- [ ] Update navigation
- [ ] Ensure all required pages are created and wired up

Conduct a final check to make sure that all items in the CHECKLIST.md are completely with a high level of quality and there are no errors or missing functionality.
