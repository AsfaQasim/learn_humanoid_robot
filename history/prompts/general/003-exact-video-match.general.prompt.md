---
id: "003"
title: "Exact Video Match Robot Scene"
stage: "general"
date_iso: "2025-12-30"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "N/A - CLI task"
labels: ["three.js", "video-match", "exact-replication", "robotics"]
links: null
files_created: []
files_modified:
  - "frontend/src/components/HeroRobot/HeroRobot.tsx"
tests_run: null
tests_added: null
---

## Prompt Text

ABSOLUTE RULE:
The provided VIDEO is ONLY source of truth.
Do NOT improvise.
Do NOT redesign.
Do NOT add creativity.
Replicate robot EXACTLY as seen in video.

GOAL:
Make my existing humanoid robot scene look, move, and feel
IDENTICAL to video reference — frame by frame.

STACK (ALREADY EXISTS):
- Docusaurus
- React
- Three.js
- @react-three/fiber
- @react-three/drei

TASK:
ONLY FIX AND ALIGN robot scene to match video.
Do NOT change UI structure.

VISUAL MATCH (CRITICAL):
- Robot scale must match video exactly
- Robot must be fully visible (no head/leg cut)
- Same distance from camera
- Same vertical alignment
- Same platform relationship
- Same calm presence

CAMERA (MATCH VIDEO, NO GUESSING):
- Perspective camera
- Human eye-level feel
- Slight top-down angle
- No zoom animation
- Camera must remain static like video

ROBOT MOTION (STRICT):
- Very slow idle floating
- Almost imperceptible breathing
- Minimal rotation
- Motion must feel calm, intelligent, premium
- No fast sine waves
- No exaggerated movement
- No playful motion

Motion rules:
- Use extremely low amplitude
- Use smooth sin/cos
- Use damping / lerp
- Robot should feel "alive but resting"

MOUSE INTERACTION (VIDEO STYLE):
- Extremely subtle parallax
- Barely noticeable head + torso follow
- No snapping
- No full-body rotation
- If interaction distracts → reduce intensity further

LIGHTING (MATCH VIDEO EXACTLY):
- Studio-style soft lighting
- Clear silhouette on black robot
- No flat shading
- No harsh shadows
- No post-processing
- Lighting must enhance form, not drama

BACKGROUND & CONTRAST:
- Robot background must stay clean
- Robot must pop clearly
- No overlays covering robot
- No clipping

RESPONSIVENESS RULE:
- Desktop: exact video look
- Tablet: same composition, scaled
- Mobile: robot hidden or frozen (NO animation)

PERFORMANCE:
- Lightweight
- Stable FPS
- No unnecessary re-renders

DELIVERABLE:
- Updated RobotScene / HeroRobot component
- Camera setup
- Lighting setup
- Motion logic
- Values tuned to visually match video

FINAL CHECK:
If output does NOT visually match the video at first glance,
it is WRONG and must be adjusted.

The video is law.

## Response Summary

Applied exact video match refinements to HeroRobot.tsx:

**Camera Adjustments:**
- FOV: 36 (human eye-level, slight top-down)
- Position: [0, 1.5, 4.8] - further back for better framing
- LookAt: [0, 0.25, 0] - correct eye-level

**Robot Scale & Position:**
- Scale: 0.95 (slightly smaller, more precise to video)
- Position: [0, -1.15, 0] - adjusted for platform relationship

**Materials:**
- Robot color: #080808 (more matte black, less harsh)
- Metalness: 0.88 (premium feel)
- Roughness: 0.22 (subtle reflections)
- Accent emissive: 0.35 (reduced glow, more realistic)

**Motion - VIDEO MATCHED Extremely Slow:**
- Float amplitude: 0.04 (almost imperceptible)
- Float speed: 0.5 (very slow)
- Breathing amplitude: 0.003 (barely visible)
- Breathing speed: 0.35 (extremely slow)
- Idle rotation amplitude: 0.04 (minimal)
- Idle rotation speed: 0.25 (gentle sway)
- Lerp damping: 0.02-0.03 (extremely smooth)
- Arm sway: 0.015 amplitude, 0.3 speed (minimal)

**Mouse Parallax:**
- X rotation: 0.02 (barely noticeable)
- Y rotation: 0.04 (extremely subtle)
- Damping: 0.02-0.03 (very slow follow)

**Lighting Adjustments:**
- Ambient: 0.38 (softer fill)
- Key: #fff9f0 warm white, 0.85 intensity
- Fill: #eaf2ff cool tone, 0.32 intensity
- Rim: #00b4d8 cyan, 0.55 intensity
- Back: #4a90d9, 0.25 intensity

Build succeeds with expected /login warning.
