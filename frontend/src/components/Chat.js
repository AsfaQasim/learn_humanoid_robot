import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

// ⚡ Change this to true if testing locally
const USE_LOCAL_BACKEND = true;

// Backend URLs
const LOCAL_BACKEND = "http://localhost:8000";
const DEPLOYED_BACKEND = "https://asfaqasim-my-chatbot.hf.space";

//  backend dynamically

const BACKEND_URL =
    process.env.NODE_ENV === "development"
        ? "http://localhost:8000"
        : "https://asfaqasim-my-chatbot.hf.space";


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
            const selection = window.getSelection().toString();
            if (selection) setSelectedText(selection);
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
            const response = await fetch(`${BACKEND_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: "123",
                    query_text: input,
                    collection_name: "my_embed"
                }),

            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();

            const botMessage = {
                id: Date.now() + 1,
                text: data.answer || data.response_text || "No response received",
                sender: 'bot',
                response_id: data.response_id,
                sources: data.sources || []
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (e) {
            setError('Failed to fetch response from chatbot. Please try again.');
            console.error(e);
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
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            alert('Feedback submitted!');
        } catch (e) {
            alert('Failed to submit feedback.');
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