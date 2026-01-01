# Implementation Plan: AI Loader & Cinematic Transitions

## 1. Scope and Dependencies
- **In Scope**: `AILoader.tsx` component, `HeroRobot.tsx` modification, CSS transitions.
- **Out of Scope**: Modifying the 3D model geometry or materials (unless needed for animation).
- **Dependencies**: React, Three.js (already in project).

## 2. Key Decisions and Rationale
- **Decision**: Create a dedicated `AILoader` component.
  - **Rationale**: Better separation of concerns and reusability.
- **Decision**: Use CSS for transitions.
  - **Rationale**: Performance optimized and easier to manage cinematic effects like blur/glow.
- **Decision**: Use a "first frame" trigger for the transition.
  - **Rationale**: Ensures the robot is actually rendered before hiding the loader.

## 3. Interfaces and API Contracts
- `AILoader` Props:
  - `isLoading`: boolean
  - `onComplete`: callback (optional)

## 4. Implementation Steps
1. Create `frontend/src/components/AILoader/AILoader.tsx`.
2. Create `frontend/src/components/AILoader/AILoader.module.css`.
3. Update `HeroRobot.tsx` to handle `isReady` state.
4. Add transition logic to `HeroRobot` wrapper.

## 5. Risk Analysis
- **Risk**: Robot rendering takes too long.
  - **Mitigation**: Ensure loader is engaging and smooth.
- **Risk**: Transition feels jarring if timed poorly.
  - **Mitigation**: Use `requestAnimationFrame` to detect first render and apply CSS classes.

## 6. Evaluation and Validation
- Manual testing on mobile and desktop.
- Verify no layout shifts during transition.
- Check "Initializing AI Robot..." text visibility.
