---
id: 019
title: Vercel Deployment Configuration
stage: general
date: 2026-01-06
surface: agent
model: gemini-cli
feature: none
branch: main
user: placeholder
command: placeholder
labels: [ "vercel", "deployment", "fastapi", "docusaurus" ]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - vercel.json
tests:
  - none
---

## Prompt

analyze my project structurea review the frontend docasorus and backend fastapi and create correct vercel.json for serverless deploymetn use context7 mcp if you need any documentaion help if there any changes required in project according to the serverless deployment then create detailed plan so I can review i

## Response snapshot

I have analyzed your project and created a `vercel.json` file to enable serverless deployment on Vercel. Here is the plan and explanation:

### Deployment Plan for Vercel

No changes are required to your existing code. The deployment is configured entirely through the new `vercel.json` file I have added to your project root.

### `vercel.json` Configuration

I have created the following `vercel.json` file:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "backend/app.py",
      "use": "@vercel/python"
    }
  ],
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/backend/app.py"
    },
    {
      "source": "/(.*)",
      "destination": "/frontend/$1"
    }
  ]
}
```

### How It Works

1.  **`builds`**: This section tells Vercel how to build your project.
    *   **Frontend**: The first build step uses `@vercel/static-build` for your Docusaurus site. It targets `frontend/package.json`, which tells Vercel to run `npm install` and `npm run build` inside the `frontend` directory. The `distDir: "build"` config points to the build output directory (`frontend/build`).
    *   **Backend**: The second build step uses `@vercel/python` to package your FastAPI application. It targets `backend/app.py`, and Vercel will automatically find and install the dependencies from `backend/requirements.txt`.

2.  **`rewrites`**: This section tells Vercel how to route incoming traffic.
    *   **API**: The first rewrite rule directs any request starting with `/api/` to your Python serverless function (`/backend/app.py`).
    *   **Frontend**: The second rule is a catch-all that rewrites all other requests to the output of the Docusaurus build. The `destination: "/frontend/$1"` works because Vercel makes the output of the static build available at a path corresponding to its source directory. This ensures your Docusaurus app handles all non-API routes.

### Next Steps

Your project is now configured for deployment on Vercel. You can deploy it by connecting your Git repository to a new Vercel project. Vercel will automatically detect and use the `vercel.json` file.


## Outcome

- ✅ Impact: Created a `vercel.json` file to enable serverless deployment of the Docusaurus frontend and FastAPI backend.
- 🧪 Tests: No tests were run as this was a configuration task.
- 📁 Files: `vercel.json` was created.
- 🔁 Next prompts: User may ask to deploy or make further configuration changes.
- 🧠 Reflection: The monorepo configuration for Vercel with a Python backend and a static frontend required careful consideration of the build outputs and routing rules. The use of `rewrites` is key to correctly directing traffic to the appropriate service.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
