# Vercel Deployment Guide

This project is configured for deployment on Vercel. Follow these steps to deploy your application successfully:

## Prerequisites

Before deploying to Vercel, ensure you have the following environment variables set in your Vercel project:

### Required Environment Variables

- `QDRANT_URL` - Your Qdrant cloud instance URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `COHERE_API_KEY` - Your Cohere API key
- `GEMINI_API_KEY` - Your Google Gemini API key (optional but recommended)

## Deployment Steps

1. **Connect your GitHub repository** to a new Vercel project
2. **Add the environment variables** listed above in the Vercel dashboard under Settings → Environment Variables
3. **Configure the build settings** (these should be detected automatically from `vercel.json`):
   - Build Command: `npm run build`
   - Output Directory: `frontend/build`
   - Install Command: `npm install`

## Architecture

The deployment consists of:
- **Frontend**: Docusaurus static site deployed as a static build
- **Backend**: FastAPI serverless functions deployed under `/api/*` routes

## Troubleshooting

If you encounter a 500 error after deployment:

1. Check the Vercel logs in your project dashboard
2. Verify all required environment variables are set
3. Ensure your Qdrant instance is accessible from external networks
4. Confirm your API keys are valid and have the necessary permissions

## API Routes

- Frontend: `https://your-project.vercel.app/`
- Chat API: `https://your-project.vercel.app/api/chat`
- Feedback API: `https://your-project.vercel.app/api/feedback`
- Health check: `https://your-project.vercel.app/api/health`

## Local Development

For local development, create a `.env.local` file in the backend directory with your environment variables:

```bash
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
GEMINI_API_KEY=your_gemini_api_key
```