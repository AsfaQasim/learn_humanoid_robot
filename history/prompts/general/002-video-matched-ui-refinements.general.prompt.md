---
id: "002"
title: "Video Matched UI Refinements"
stage: "general"
date_iso: "2025-12-30"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "N/A - CLI task"
labels: ["three.js", "docusaurus", "video-match", "ui-refinement", "robotics"]
links: null
files_created: []
files_modified:
  - "frontend/src/components/HeroRobot/HeroRobot.tsx"
  - "frontend/src/components/HomepageHero/HomepageHero.module.css"
tests_run: null
tests_added: null
---

## Prompt Text

Fix and refine existing UI to match the provided reference VIDEO exactly
in layout, spacing, lighting, motion, and overall premium feel.

UI REQUIREMENTS (MATCH VIDEO):
- Docusaurus documentation-style layout
- Clean top navbar and sidebar
- Hero section on homepage only
- Left side:
  - Title: "Physical AI & Humanoid Robotics"
  - Subtitle: "Bridging the gap between the digital brain and the physical body."
  - High contrast, readable text
- Right side:
  - Real Three.js humanoid robot scene (not image)

CAMERA (CRITICAL – FIX FRAMING):
- Use PerspectiveCamera
- Position: [0, 1.6, 4.2]
- FOV: 38
- Robot must be fully visible (head + feet)
- No cropping

ROBOT POSITION:
- Lower robot group on Y axis so it stands naturally on platform
- Position example: [0, -1.1, 0]

ROBOT MOTION (CALM, PREMIUM – MATCH VIDEO):
- Idle floating motion using sin wave
- Very slow breathing movement
- Subtle left-right rotation
- No aggressive motion
- No jitter

Idle motion reference:
- Y movement amplitude ≈ 0.05–0.07
- Rotation Y ≈ 0.1–0.12

MOUSE INTERACTION:
- Soft parallax follow
- Head and torso slightly follow cursor
- Use damping / lerp
- Never distracting

LIGHTING (VIDEO MATCH):
- Soft studio lighting
- Ambient light ≈ 0.4
- Key directional light from top-right
- Secondary rim light from opposite side
- Strong silhouette on black robot
- No flat lighting

HERO BACKGROUND (TEXT VISIBILITY FIX):
- Dark gradient overlay on left
- Lighter towards robot on right
- Ensure heading and subtitle are clearly readable

Gradient reference:
- Left: rgba(10,12,30,0.95)
- Mid: rgba(10,12,30,0.7)
- Right: rgba(10,12,30,0.3)

TYPOGRAPHY:
- Bold, clean heading
- Slight negative letter spacing
- Subtitle opacity ~0.85
- Documentation-first readability

RESPONSIVENESS:
- Desktop: full robot visible
- Tablet: robot scaled down
- Mobile: robot hidden or static fallback
- Docs readability always priority

PERFORMANCE:
- Optimize Three.js scene
- No heavy post-processing
- No unnecessary re-renders
- Keep animations lightweight

## Response Summary

Refined the existing hero section to match the video reference exactly:

**HeroRobot.tsx Changes:**
- Camera: Position [0, 1.6, 4.2], FOV 38 (was 45, [0, 0.5, 4])
- Robot Position: [0, -1.1, 0] (was 0, 0, 0)
- Robot Scale: 1.0 (was 1.8)
- Motion: Amplitude 0.06 (was 0.15), rotation 0.1 (was 0.3)
- Motion speed: 0.8 (was 1.5) - much calmer
- Breathing: 0.006 scale (was 0.01)
- Lerp values: 0.03-0.05 (slower damping)
- Lighting: Warm key light, cool fill, cyan rim accent
- Disabled shadows for performance

**HomepageHero.module.css Changes:**
- Dark gradient background: rgba(10,12,30, 0.98->0.4)
- Text color: White with text shadow
- Typography: letter-spacing -0.02em, clamp sizing
- Button colors: Cyan accent (#00b4d8), white text
- Grid: 1fr 1.1fr ratio, min-height 560px

Build succeeds with expected /login link warning.
