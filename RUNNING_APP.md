# Running the Application

This document explains how to run the Physical AI & Humanoid Robotics textbook application with both backend and frontend.

## Project Structure

```
project-root/
├── backend/              # FastAPI backend
├── frontend/             # Docusaurus frontend
├── start_both.bat        # Development: Start both services
├── build_and_serve_prod.bat  # Production: Build and serve
└── RUNNING_APP.md        # This file
```

## Development Mode

### Option 1: Using the combined script (Recommended)

1. Open Command Prompt or PowerShell in the project root directory
2. Run the combined startup script:
```bash
start_both.bat
```

This will:
- Start the backend server at `http://localhost:8000`
- Start the frontend development server at `http://localhost:3000`
- Both windows will open automatically

### Option 2: Manual setup

1. **Start the backend:**
```bash
cd backend
run_dev.bat
```

2. **Start the frontend:**
In a new terminal/command prompt:
```bash
cd frontend
npm start
```

## Production Mode

To build and serve the application in production:

1. Run the production build script:
```bash
build_and_serve_prod.bat
```

This will:
- Build the frontend (Docusaurus site)
- Copy the built files to the backend's static directory
- Start the backend server which will serve both API and frontend

The application will be available at `http://localhost:8000`

## Manual Production Build

If you prefer to do it manually:

1. **Build the frontend:**
```bash
cd frontend
npm run build
```

2. **Copy build to backend:**
```bash
# From project root
xcopy /E /I /Y frontend\build backend\static\
```

3. **Start the backend:**
```bash
cd backend
run_app.bat
```

## Troubleshooting

### Common Issues

1. **Frontend not connecting to backend:**
   - Ensure backend is running on `http://localhost:8000`
   - Check that the API endpoints are accessible

2. **Port conflicts:**
   - Backend runs on port 8000
   - Frontend development server runs on port 3000
   - Ensure these ports are available

3. **Chat component not working:**
   - Verify that `Chat.js` is properly integrated
   - Check browser console for errors
   - Ensure backend API endpoints are accessible

### Frontend Chat Component

The frontend includes a fully functional chat component:
- Located in `frontend/src/components/Chat.js`
- Integrated into the layout via `frontend/src/theme/Layout.js`
- Connects to backend API at `http://localhost:8000/chat`
- Includes feedback functionality for responses

## Environment Variables

Make sure your backend has the required environment variables set in `backend/.env`:
```
GEMINI_API_KEY=your_gemini_api_key
QDRANT_HOST=your_qdrant_host
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
```