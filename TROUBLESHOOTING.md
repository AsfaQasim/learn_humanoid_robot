# Troubleshooting Guide: Backend-Frontend Connection Issues

## Issue: "Failed to fetch" Error in Chat.js

### Root Cause
The frontend cannot connect to the backend API at `http://localhost:8000/chat`. This happens when:

1. The backend server is not running
2. The backend server is not accessible at the expected URL
3. Network/firewall issues
4. CORS policy violations
5. Incorrect environment variables

### Solutions

#### 1. Verify Backend is Running
- Open Command Prompt in the project root
- Navigate to the backend directory: `cd backend`
- Start the server: `python run_server.py`
- Verify it's running at: `http://localhost:8000/health`

#### 2. Check Environment Variables
Create a `.env` file in the `backend` directory with:
```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

#### 3. Test the API Endpoint
Run the test script to verify connectivity:
```
cd backend
python test_api.py
```

#### 4. Check Port Availability
- Ensure port 8000 is not used by other applications
- Check with: `netstat -an | find "8000"`

#### 5. Firewall/Network Issues
- Temporarily disable firewall to test
- Check if antivirus is blocking connections

#### 6. CORS Issues
The backend app.py has been updated to allow all origins during development.

### Quick Setup Commands

1. Start backend:
   ```
   cd backend
   python run_server.py
   ```

2. In a new terminal, start frontend:
   ```
   cd frontend
   npm start
   ```

3. Test API connectivity:
   ```
   cd backend
   python test_api.py
   ```

### Debugging Steps

1. Open browser DevTools (F12)
2. Go to Network tab
3. Try sending a message in the chat
4. Look for the failed request to `/chat`
5. Check the exact error message

### Common Error Messages and Solutions

- "Failed to fetch": Backend server is not running or unreachable
- "CORS error": Backend CORS settings need adjustment
- "404 Not Found": Backend route doesn't exist
- "Connection refused": Port is closed or blocked

### Verification Checklist

- [ ] Backend server running on http://localhost:8000
- [ ] Environment variables properly set
- [ ] `/health` endpoint returns status
- [ ] `/chat` endpoint accepts POST requests
- [ ] Frontend can make requests to backend
- [ ] No CORS errors in browser console