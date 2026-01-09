---
id: 023
title: Add feedback endpoint
stage: general
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: DENZEN COMPUTER
command: interactive
labels: [api,fastapi,feedback]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/app.py
tests:
 - python -m py_compile backend/app.py
---

## Prompt

Add /feedback endpoint to backend

## Response snapshot

Implemented POST /feedback in backend/app.py to accept {response_id, feedback} from the frontend thumbs up/down buttons. The endpoint validates feedback is either 1 or -1 and logs it server-side. Also added response_id generation to /chat responses so the frontend can reference messages when submitting feedback.

## Outcome

- ✅ Impact: Frontend feedback buttons now have a matching backend endpoint.
- 🧪 Tests: Python syntax check passed.
- 📁 Files: Updated backend/app.py.
- 🔁 Next prompts: If you want feedback stored persistently, choose storage (file, db, qdrant payload, etc.).
- 🧠 Reflection: Minimal logging-based implementation keeps changes small while unblocking UI.

## Evaluation notes (flywheel)

- Failure modes observed: Previously, /feedback was called by frontend but no backend route existed, causing user-visible failures.
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add persistent feedback storage and include response_id in UI state.
