import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

// Backend URLs - using window object for client-side environment detection
const LOCAL_BACKEND = "http://localhost:8000";
const PROD_BACKEND = "https://learn-humanoid-robot-mz3d.vercel.app";

// Determine backend URL based on environment and availability
let BACKEND_URL;
if (typeof window !== 'undefined') {
    // Client-side (browser)
    // Check if we're in development mode by checking for webpack dev server
    const isDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    BACKEND_URL = isDev ? LOCAL_BACKEND : PROD_BACKEND;
} else {
    // Server-side (if applicable)
    BACKEND_URL = LOCAL_BACKEND; // Default to local during build
}

console.log("Backend URL:", BACKEND_URL); // Debug log


// Helper function to get authentication headers
const getAuthHeaders = () => {
    // Check for various possible authentication tokens
    const token = localStorage.getItem('authToken') ||
                  sessionStorage.getItem('authToken') ||
                  localStorage.getItem('access_token') ||
                  sessionStorage.getItem('access_token');

    if (token) {
        return {
            'Authorization': `Bearer ${token}`,
            'X-Auth-Token': token
        };
    }
    return {};
};

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [selectedText, setSelectedText] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        setMessages([{
            id: Date.now(),
            text: "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant. I can help you with questions about robotics, AI, physical computing, and related topics. What would you like to know about the textbook content?",
            sender: 'bot'
        }]);

        const handleMouseUp = () => {
            const selection = window.getSelection().toString().trim();
            if (selection.length > 0) setSelectedText(selection);
        };
        window.addEventListener('mouseup', handleMouseUp);
        return () => window.removeEventListener('mouseup', handleMouseUp);
    }, []);

    useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { id: Date.now(), text: input, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);
        setError(null);

        try {
            // Prepare request configuration
            const requestConfig = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add authentication header if available
                    ...getAuthHeaders(),
                    // Additional headers that might help with CORS
                    'Accept': 'application/json',
                },
                body: JSON.stringify({
                    session_id: "123",
                    query_text: input,
                    collection_name: "my_embed"
                }),
            };

            console.log(`Attempting to connect to: ${BACKEND_URL}/chat`);
            console.log('Request config:', requestConfig);

            // Make the API call with timeout
            // Increase timeout to handle potential delays in API response
            const controller = new AbortController();
            const timeoutId = setTimeout(() => {
                console.log('Request timeout after 60 seconds');
                controller.abort();
            }, 60000); // 60 second timeout

            const response = await fetch(`${BACKEND_URL}/chat`, {
                ...requestConfig,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            console.log(`Response status: ${response.status}`);
            console.log(`Response OK: ${response.ok}`);

            if (!response.ok) {
                const errorData = await response.text();
                console.error('Server responded with error:', errorData);

                // Handle different status codes appropriately
                if (response.status === 401) {
                    setError('Unauthorized: Please check your authentication credentials.');
                } else if (response.status === 403) {
                    setError('Forbidden: You do not have permission to access this resource.');
                } else if (response.status === 404) {
                    setError('Endpoint not found. Make sure the backend server is running and the API endpoint exists.');
                } else if (response.status >= 500) {
                    setError(`Server error (${response.status}): The backend server encountered an error.`);
                } else {
                    setError(`HTTP error! status: ${response.status}, message: ${errorData}`);
                }

                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData}`);
            }

            // Check if response is valid JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                const textResponse = await response.text();
                console.warn('Non-JSON response received:', textResponse);
                throw new Error(`Expected JSON response but got: ${textResponse}`);
            }

            const data = await response.json();
            console.log('Response data:', data);

            const botMessage = {
                id: Date.now() + 1,
                text: data.answer || data.response_text || "No response received",
                sender: 'bot',
                response_id: data.response_id,
                sources: data.sources || []
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (e) {
            console.error('Chat API Error:', e);
            console.error('Detailed error info:', {
                message: e.message,
                name: e.name,
                stack: e.stack,
                isAborted: e.name === 'AbortError',
                isNetworkError: e.name === 'TypeError' && e.message.includes('fetch')
            });

            // Handle different types of errors
            if (e.name === 'AbortError') {
                setError('Request timed out. The server took too long to respond. This might be due to missing API keys or slow processing.');
            } else if (e.message.includes('404')) {
                setError('Chat endpoint not found. Make sure the backend server is running on port 8000. Run: "cd backend && python run_server.py"');
            } else if (e.message.includes('fetch')) {
                if (e.message.includes('Failed to fetch')) {
                    setError('Unable to connect to the backend server. Possible causes:\n- Backend server is not running\n- Network connectivity issue\n- CORS policy violation\n- SSL certificate issue\n\nCheck browser console for more details.');
                } else {
                    setError('Network error occurred while connecting to the backend server. Check browser console for more details.');
                }
            } else if (e.message.includes('JSON')) {
                setError('Invalid response format received from the server. The server may not be returning valid JSON.');
            } else {
                setError(`Failed to fetch response from chatbot: ${e.message}`);
            }
        } finally {
            setLoading(false);
            setSelectedText('');
        }
    };

    const handleKeyPress = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } };

    const handleFeedback = async (responseId, feedback) => {
        try {
            const response = await fetch(`${BACKEND_URL}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ response_id: responseId, feedback }),
            });
            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData}`);
            }
            alert('Feedback submitted!');
        } catch (e) {
            console.error('Feedback API Error:', e);
            if (e.message.includes('404')) {
                alert('Feedback endpoint not found. Make sure the backend server is running on port 8000. Run: "cd backend && python run_server.py"');
            } else if (e.message.includes('fetch')) {
                alert('Unable to connect to the backend server for feedback submission.');
            } else {
                alert(`Failed to submit feedback: ${e.message}`);
            }
            console.error(e);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map(msg => (
                    <div key={msg.id} className={`message message--${msg.sender}`}>
                        <div className="message-content">{msg.text}</div>
                        {msg.sender === 'bot' && msg.sources?.length > 0 && (
                            <div className="message-extensions">
                                <div className="sources-section">
                                    <details className="sources-details">
                                        <summary>Sources ({msg.sources.filter(s => s && typeof s === 'string').length})</summary>
                                        <ul className="sources-list">
                                            {msg.sources.filter(s => s && typeof s === 'string')
                                                .map((source, idx) => (
                                                    <li key={idx} className="source-item">
                                                        {source.length > 150 ? source.substring(0, 150) + '...' : source}
                                                    </li>
                                                ))}
                                        </ul>
                                    </details>
                                </div>
                                <div className="feedback-buttons">
                                    <button className="feedback-btn feedback-btn--positive" onClick={() => handleFeedback(msg.response_id, 1)} title="Helpful">👍</button>
                                    <button className="feedback-btn feedback-btn--negative" onClick={() => handleFeedback(msg.response_id, -1)} title="Not helpful">👎</button>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div className="message message--bot message--loading">
                        <div className="message-content"><div className="loading-dots"><span>.</span><span>.</span><span>.</span></div></div>
                    </div>
                )}
                {error && <div className="message message--error"><div className="message-content">{error}</div></div>}
                <div ref={messagesEndRef} />
            </div>
            {selectedText && (
                <div className="selected-text-container">
                    <p><strong>Selected Text:</strong></p>
                    <p className="selected-text-content"><em>{selectedText}</em></p>
                </div>
            )}
            <div className="chat-input-container">
                <textarea
                    ref={inputRef}
                    className="chat-input"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    disabled={loading}
                    rows={1}
                    style={{ height: 'auto' }}
                />
                <button className="send-button" onClick={handleSend} disabled={loading || input.trim() === ''}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
};

export default Chat;