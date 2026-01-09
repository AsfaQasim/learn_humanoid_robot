---
id: 022
title: Fix chatbot sources selected text display
stage: general
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: DENZEN COMPUTER
command: interactive
labels: [rag,frontend,backend,formatting]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/rag_service.py
 - frontend/src/components/Chat.js
 - backend/app.py
tests:
 - python -m py_compile backend/rag_service.py
 - python -m py_compile backend/app.py
 - node -c frontend/src/components/Chat.js
---

## Prompt

ros
I don't know.
Sources (5)
ROS 2 Nodes are the fundamental building blocks of the Robot Operating System 2 (ROS 2) architecture. A node is an executable that uses ROS 2 to commu...
A ROS 2 node is an instance of a process that may subscribe to or publish to a topic. Nodes are the primary computational unit in ROS 2 and are used t...
ROS 2 provides Quality of Service (QoS) settings to control the behavior of topic communication: - **Reliability**: Best effort or reliable delivery ...
self.ros = roslibpy.Ros(host=rosbridge_addr, port=rosbridge_port) self.ros.run()
ROS 2 Launch files provide a powerful way to manage complex robotic systems by launching multiple nodes with specific configurations simultaneously. T...
👍
👎
Selected Text:

 still my chatbot response look like this solve this

## Response snapshot

Identified that the UI (frontend/src/components/Chat.js) displays whatever the backend returns in the `answer` field. Added backend-side cleaning in backend/rag_service.py to strip accidental model output that looks like debug/metadata sections (e.g., "Sources (...)" and "Selected Text:"). Also adjusted the frontend to use the same-origin Vercel API route ("/api") in production so it hits backend/app.py on Vercel instead of an external hf.space backend that may be returning the noisy answer text. Minor UI improvement: trim selected text before displaying.

## Outcome

- ✅ Impact: Cleaner chatbot responses; sources remain in the expandable Sources panel instead of leaking into the answer text.
- 🧪 Tests: Python syntax checks passed; JS syntax check passed.
- 📁 Files: Updated backend/rag_service.py, backend/app.py, and frontend/src/components/Chat.js.
- 🔁 Next prompts: Deploy and confirm the frontend is calling /api/chat; verify that the answer no longer contains embedded "Sources (...)" lines.
- 🧠 Reflection: The stable fix is (1) correct backend routing and (2) cleaning model output as a last-resort guardrail.

## Evaluation notes (flywheel)

- Failure modes observed: Frontend was pointing to an external backend in production; model output could include metadata-like sections that should be separated from answer.
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add an explicit instruction in the LLM prompt to never output "Sources"/"Selected Text" sections (defense-in-depth).
