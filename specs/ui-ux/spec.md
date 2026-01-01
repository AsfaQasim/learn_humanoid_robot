# Specification: Futuristic AI Circular Loader & Transitions

## Overview
Implement a high-end, futuristic circular loader for the main landing page that signals an AI experience is initializing. The loader must transition smoothly into the 3D robot once it is fully rendered.

## User Requirements
- Centered circular animation in the middle of the screen.
- Smooth rotation, pulse, or glow with futuristic AI aesthetic.
- Text: "Initializing AI Robot..."
- Cinematic transition (loader fades/scales out, robot fades/zooms in).
- Fully responsive across devices.
- Tied to the actual loading state of the robot.

## Technical Requirements
- **Loader Component**: A standalone React component for the futuristic loader.
- **State Management**: Track `isReady` state in `HeroRobot.tsx` to trigger transitions.
- **CSS Animations**: Use CSS for performance-optimized transitions and animations.
- **Transitions**:
  - Loader: `opacity: 0`, `transform: scale(0.9)`
  - Robot: `opacity: 1`, `transform: scale(1.1)` (transitioning to `scale(1)`)

## Acceptance Criteria
- [ ] Loader is visible immediately on page load.
- [ ] Loader shows "Initializing AI Robot..." text.
- [ ] Loader performs a smooth circular animation with glowing effects.
- [ ] Robot is hidden until the Three.js scene is ready.
- [ ] Smooth transition happens once the robot is ready (no layout shifts).
- [ ] Transition is cinematic (fade + scale).
- [ ] Responsive on mobile and desktop.
