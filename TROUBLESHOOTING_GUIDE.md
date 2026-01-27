# Troubleshooting "Failed to fetch" Errors

## Overview
This guide addresses the "Failed to fetch" error commonly encountered when the frontend cannot communicate with the backend API.

## Root Causes and Solutions

### 1. Backend Server Not Running
**Symptoms:** 
- Console error: "Failed to fetch"
- Network tab shows connection refused

**Solutions:**
- Start the backend server: `cd backend && python run_server.py`
- Verify the server is running at http://localhost:8000
- Check that the port is not used by another application

### 2. CORS (Cross-Origin Resource Sharing) Issues
**Symptoms:**
- Console error: "Access to fetch at 'http://localhost:8000/chat' from origin 'http://localhost:3000' has been blocked by CORS policy"
- Network tab shows preflight OPTIONS request failing

**Solutions:**
- Backend CORS is now configured to allow localhost origins
- Check that the backend app.py has proper CORS middleware
- Verify that the frontend is making requests to the correct origin

### 3. Incorrect API Endpoint URL
**Symptoms:**
- Console error: "Failed to fetch"
- Network tab shows 404 or connection timeout

**Solutions:**
- Verify BACKEND_URL in Chat.js matches your backend server address
- Use environment variables: REACT_APP_API_URL or NEXT_PUBLIC_API_URL
- Check that the endpoint path (/chat) exists on the backend

### 4. Authentication Issues
**Symptoms:**
- Console error: "Failed to fetch" or 401/403 status codes
- Requests fail after initial setup

**Solutions:**
- Ensure authentication tokens are properly stored and sent
- Check that Authorization headers are included in requests
- Verify token validity and refresh mechanisms

### 5. Network Connectivity Problems
**Symptoms:**
- Intermittent "Failed to fetch" errors
- Works sometimes, fails other times

**Solutions:**
- Check firewall settings
- Verify network connectivity
- Try disabling VPN if active
- Check proxy settings

## Verification Steps

### 1. Test Backend Directly
```bash
curl -X GET http://localhost:8000/health
```

### 2. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "query_text": "hello", "collection_name": "document_embeddings"}'
```

### 3. Run Comprehensive Test
```bash
cd backend
python comprehensive_test.py
```

### 4. Check Browser Developer Tools
- Open Network tab
- Send a message in the chat
- Look for the failing request
- Note the exact error message and status code

## Environment Configuration

### Backend (.env file)
```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local file)
```
REACT_APP_API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Quick Fixes Checklist

- [ ] Backend server running on http://localhost:8000
- [ ] Environment variables properly configured
- [ ] CORS headers properly set on backend
- [ ] Frontend pointing to correct backend URL
- [ ] No browser extensions blocking requests
- [ ] Firewall not blocking local connections
- [ ] Antivirus not interfering with local traffic

## Debugging Commands

### Check if backend is running
```bash
netstat -an | find "8000"
```

### Test connectivity
```bash
ping localhost
telnet localhost 8000  # Windows
```

### View server logs
Keep the backend terminal open to monitor incoming requests and errors.

## Production Considerations

For production deployments:
- Remove wildcard CORS origins (*)
- Use proper authentication
- Implement proper error boundaries
- Add request/response logging
- Monitor API response times
- Implement retry mechanisms for failed requests