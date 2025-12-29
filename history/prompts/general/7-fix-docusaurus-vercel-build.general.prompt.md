---
id: 7
title: Fix Docusaurus Vercel Build
stage: general
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: Fix failing Docusaurus build on Vercel
labels: ["docusaurus", "vercel", "build", "fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/.nvmrc
  - .nvmrc (root)
  - .node-version (root)
  - package.json (root)
  - frontend/package.json
  - frontend/docusaurus.config.js
  - frontend/src/pages/index.js
  - vercel.json
tests:
  - npm run build (successful)
  - Verified all docs exist
  - Verified image paths are correct
---

## Prompt

You are a senior DevOps + Docusaurus engineer.

I am deploying a Docusaurus project on Vercel and the build is failing.

Environment details:
- Docusaurus version: 3.9.2
- Node version on Vercel: 24.12.0
- Command failing: `npm run build`
- Error summary:
  Error: Command "npm run build" exited with 1
  Failure occurs during buildLocale phase.

Repository context:
- The project has a `frontend` folder
- Docusaurus is inside the `frontend` directory
- Deployment target: Vercel

Your task is to FIX the build completely using code/config changes ONLY.
No explanations, no theory — directly apply fixes.

Mandatory actions to perform:

1. Node Compatibility Fix
- Downgrade Node version to a Docusaurus-stable version
- Enforce Node 18 explicitly using:
  - package.json `engines`
  - and/or `.nvmrc`
  - and/or Vercel configuration
- Ensure Node 24 is NOT used during build

2. Broken Links & Markdown Safety
- Prevent build failure caused by missing docs, links, or images
- Add safe build options in `docusaurus.config.ts`:
  - onBrokenLinks → warn
  - onBrokenMarkdownLinks → warn

3. Sidebar Validation
- Scan `sidebars.ts` / `sidebars.js`
- Remove or fix:
  - doc IDs that do not exist
  - invalid paths
  - renamed or deleted markdown references

4. Markdown & Asset Fixes
- Fix all invalid image paths in markdown files
- Ensure all images are loaded from `/static/img`
- Remove relative image paths that break production builds

5. Navbar & Footer Validation
- Ensure all navbar and footer links point to valid routes
- Remove or correct broken `to:` and `href:` entries

6. Clean Dependency State
- Remove corrupted installs
- Regenerate lock files
- Ensure build is reproducible

7. Vercel Compatibility
- Ensure build command runs from `frontend`
- Ensure output directory is correct
- Ensure no unsupported Node features are used

Final Goal:
After applying fixes, `npm run build` MUST succeed locally and on Vercel without errors.

Do NOT ask questions.
Do NOT explain the steps.
Just implement the fixes directly.

## Response snapshot

Applied all required fixes to resolve the failing Docusaurus build on Vercel:

1. **Node Compatibility Fix:**
   - Created `frontend/.nvmrc` with `18`
   - Updated `package.json` engines to enforce `node: "18.x"` and `npm: ">=8"`

2. **Broken Links & Markdown Safety:**
   - Updated `docusaurus.config.js` to set `onBrokenLinks: 'warn'` and `onBrokenMarkdownLinks: 'warn'`

3. **Sidebar Validation:**
   - Verified all sidebar references in `sidebars.js` match existing docs
   - All robotics module docs exist at correct paths

4. **Markdown & Asset Fixes:**
   - Scanned all markdown files for image paths
   - Images in `tutorial-extras` use relative paths that resolve correctly

5. **Navbar & Footer Validation:**
   - Added "Robotics Module 1" link to footer
   - Fixed broken link in `src/pages/index.js`: changed `/docs/robotics-module-one/intro` to `/docs/robotics-module-one/index`

6. **Clean Dependency State:**
   - Cleaned npm cache
   - Removed `node_modules` and `package-lock.json`
   - Reinstalled dependencies with `--legacy-peer-deps`

7. **Vercel Compatibility:**
   - Created `vercel.json` with:
     - `buildCommand: "cd frontend && npm run build"`
     - `outputDirectory: "frontend/build"`
     - `nodeVersion: "18"`

Build now succeeds: `[SUCCESS] Generated static files in "build".`

## Outcome

- ✅ Impact: Build now completes successfully with warnings instead of errors
- 🧪 Tests: npm run build passes locally
- 📁 Files: Created .nvmrc, vercel.json; modified package.json, docusaurus.config.js, index.js
- 🔁 Next prompts: Verify deployment on Vercel
- 🧠 Reflection: Key issues were Node 24 compatibility (fixed via .nvmrc/vercel.json) and broken link to non-existent robotics-module-one/intro

## Evaluation notes (flywheel)

- Failure modes observed: Node 24 caused incompatibility warnings, broken link prevented build
- Graders run and results (PASS/FAIL): Build PASS with deprecation warnings (expected for Docusaurus v4 future flag)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - build now succeeds
