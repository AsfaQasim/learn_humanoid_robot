# Physical AI & Humanoid Robotics Textbook

This is a comprehensive textbook application featuring a Docusaurus-based frontend with integrated chatbot functionality powered by a FastAPI backend.

## Project Structure

- **Backend**: FastAPI application in the `backend/` directory
- **Frontend**: Docusaurus site in the `frontend/` directory
- **Chat Integration**: React-based chat components in `frontend/src/components/`

## Running the Application

See [RUNNING_APP.md](RUNNING_APP.md) for detailed instructions on how to run the application in both development and production modes.

### Quick Start (Development)

1. Start both services with the combined script:
   ```bash
   start_both.bat
   ```

2. The backend will be available at `http://localhost:8000`
3. The frontend will be available at `http://localhost:3000`

### Production Build

To build and serve the application for production:
```bash
build_and_serve_prod.bat
```

The application will be served from `http://localhost:8000`

## Features

- Interactive textbook content with Docusaurus documentation framework
- AI-powered chatbot for answering questions about robotics and AI
- Source citation and feedback system for chat responses
- Responsive design for all device sizes 
