---
id: 020
title: Vercel deployment configuration
stage: general
date_iso: 2026-01-07
model: sonnet-4.5-20250929
feature: none
branch: main
user: User
command: npm install (frontend)
surface: agent
labels:
  - npm
  - frontend
  - install
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/package.json
  - frontend/package-lock.json
tests_yaml: []
prompt_text: use context7 mcp to review the correct configration for my backend with my frontend my frontend is working fine do not make any changes in it just need some change with vercel.json for the backend I wnat backend to be at /api end point and frontend to correctly communicate with it
response_text: Updated vercel.json with correct routing: changed /backend/app.py to /backend/app for Python runtime, and /frontend/$1 to /frontend/build/$1 to point to Docusaurus build output. Also noted CORS needs updating in backend/app.py for production Vercel domain.
outcome: Successfully updated vercel.json configuration for proper backend/frontend routing on Vercel deployment.
evaluation: |
  - vercel.json now correctly routes /api/* to backend/app (FastAPI)
  - Static files correctly routed to frontend/build/
  - No changes made to frontend code as requested
