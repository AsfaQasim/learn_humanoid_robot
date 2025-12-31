---
id: "001"
title: "Three.js Hero Robot Integration"
stage: "general"
date_iso: "2025-12-30"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "N/A - CLI task"
labels: ["three.js", "docusaurus", "react", "robotics", "hero-section"]
links: null
files_created:
  - "frontend/src/components/HeroRobot/HeroRobot.tsx"
  - "frontend/src/components/HeroRobot/index.ts"
  - "frontend/src/components/HomepageHero/HomepageHero.tsx"
  - "frontend/src/components/HomepageHero/HomepageHero.module.css"
  - "frontend/src/components/HomepageHero/index.ts"
files_modified:
  - "frontend/package.json"
  - "frontend/docusaurus.config.js"
  - "frontend/src/pages/index.js"
  - "frontend/src/css/custom.css"
tests_run: null
tests_added: null
---

## Prompt Text

Build a Docusaurus-based documentation website UI identical in style
to official Docusaurus docs, while integrating a premium Three.js humanoid robot
scene in the hero section.

TECH STACK:
- Docusaurus v3
- React
- Tailwind CSS (optional utility layer)
- Three.js
- @react-three/fiber
- @react-three/drei
- Context-7 MCP compatible
- 21st.dev optimized

UI STYLE (VERY IMPORTANT):
- Must look exactly like Docusaurus official docs
- Clean documentation layout
- Left sidebar navigation
- Top navbar with:
  - Physical AI & Humanoid Robotics
  - Course Content
  - About
  - GitHub
  - Login / Register
- White background
- Neutral typography
- No heavy animations in docs area

HERO SECTION (DOCUSAURUS HOMEPAGE):
- Title:
  "Physical AI & Humanoid Robotics"
- Subtitle:
  "Bridging the gap between the digital brain and the physical body."
- Two column layout inside Docusaurus HomepageHero

RIGHT SIDE (3D ROBOT SCENE):
- Embed a Three.js Canvas inside the hero
- Real 3D humanoid robot (not image)
- Black futuristic material
- Idle floating animation
- Subtle breathing motion
- Mouse-based parallax rotation
- Smooth damping
- Performance optimized for docs site

THREE.JS SCENE DETAILS:
- Perspective camera
- Soft studio lighting
- Ambient + key + rim light
- Shadows enabled but optimized
- useFrame for animation loop
- Disable heavy post-processing

RESPONSIVENESS:
- Robot hides or scales down on mobile
- Docs readability always priority

CODE QUALITY:
- Robot scene isolated in HeroRobot.tsx
- Clean React components
- No pollution of docs markdown
- Production ready

OUTPUT:
- Docusaurus homepage layout
- HeroRobot Three.js component
- Proper integration with Docusaurus theme
- Styling consistent with docs UI

## Response Summary

Successfully implemented a premium Three.js humanoid robot hero section for Docusaurus documentation site:

1. **Dependencies Added**: three, @react-three/fiber, @react-three/drei to package.json
2. **HeroRobot.tsx**: Created vanilla Three.js 3D humanoid robot component with:
   - Futuristic black metallic material with glowing cyan accents
   - Idle floating and breathing animations
   - Mouse-based parallax rotation with smooth damping
   - Soft studio lighting (ambient, key, fill, rim, back lights)
   - Contact shadows
   - SSR-compatible (client-only rendering)
3. **HomepageHero.tsx**: Two-column layout component matching Docusaurus style
4. **Updated docusaurus.config.js**: Configured navbar with requested items
5. **Custom.css**: Added hero styling and navbar login button styles
6. **Updated index.js**: Integrated HomepageHero component into homepage

The build succeeded with only expected warnings about the /login link (not yet implemented).
