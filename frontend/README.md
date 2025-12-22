# Physical AI & Humanoid Robotics Textbook

This website contains the Physical AI & Humanoid Robotics Textbook, built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## About This Textbook

This textbook covers the fundamental concepts of AI-powered humanoid robotics, with a focus on ROS 2 as the "nervous system" of robotic systems. The first module covers core ROS 2 concepts including nodes, topics, services, Python integration, URDF modeling, and advanced ROS 2 features.

## Chatbot Integration

A RAG chatbot has been integrated into the frontend to answer questions about the textbook content.

## Installation

```bash
npm install
```

## Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Available Scripts

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve

# Lint markdown files
npm run lint:md

# Clear Docusaurus cache
npm run clear

# Validate module word count
node scripts/validate-module-word-count.js
```

## Content Structure

The textbook content is organized in the `docs/` directory, with Module 1 (The Robotic Nervous System) located at `docs/1-robotics-module-one/`. Each module is further divided into chapters and lessons.

## Deployment

Using SSH:

```bash
USE_SSH=true npm run deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> npm run deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
