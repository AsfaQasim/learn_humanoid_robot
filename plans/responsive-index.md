# Plan: Make index.js Responsive

The goal is to make the `index.js` page (the landing page) fully responsive. Currently, it uses inline styles for the hero section which don't adapt well to smaller screens (e.g., the 3D robot scene overlaps text on mobile, and grid layouts remain fixed-column).

## User Review Required

> [!IMPORTANT]
> I will shift the inline styles in `index.js` to use CSS classes from `index.module.css` where media queries are already defined, and add new responsive rules to handle the layout transition from side-by-side (desktop) to stacked (mobile).

## Proposed Changes

### 1. `frontend/src/pages/index.js`
- Replace inline styles with CSS module classes from `index.module.css`.
- Add a container class to wrap the Hero section for better layout management.
- Ensure the `Spline` component and text section are wrapped in a way that allows them to stack on mobile.

### 2. `frontend/src/pages/index.module.css`
- Add/Update styles for the hero section to support a flex or grid layout that changes direction on mobile.
- **Hero Section**:
    - Desktop: `flex-direction: row` (Text left, Robot right).
    - Mobile (< 996px): `flex-direction: column-reverse` (Text top, Robot bottom or hidden/resized).
- **Feature Section Grid**:
    - Update the 3-column / 2-column grid to be `1fr` on mobile.
- **Robot Container**:
    - Adjust height and positioning for mobile so it doesn't cover the text.

## Critical Files
- `frontend/src/pages/index.js`
- `frontend/src/pages/index.module.css`

## Verification Plan
### Automated Tests
- Since this is a UI layout change, I will verify by checking that the CSS classes are correctly applied.
### Manual Verification
- Verify layout at >1024px (Desktop).
- Verify layout at 768px (Tablet - should stack or adjust).
- Verify layout at <480px (Mobile - stacked, buttons full width).
