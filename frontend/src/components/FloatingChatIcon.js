import React, { useState, useEffect } from 'react';
import Chat from './Chat';
import './FloatingChatIcon.css';

const FloatingChatIcon = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    return () => setIsMounted(false);
  }, []);

  const toggleChat = () => {
    if (isMounted) {
      setIsOpen(!isOpen);
    }
  };

  const closeChat = () => {
    if (isMounted) {
      setIsOpen(false);
    }
  };

  // Always render button to ensure it stays visible
  return (
    <>
      {/* Always render chat window when open */}
      {isOpen && (
        <div className="chat-overlay" onClick={closeChat}>
          <div className="chat-window" onClick={(e) => e.stopPropagation()}>
            <div className="chat-header">
              <span>AI Assistant</span>
              <button className="close-btn" onClick={closeChat} aria-label="Close chat">
                ×
              </button>
            </div>
            <div className="chat-content">
              <Chat />
            </div>
          </div>
        </div>
      )}
      {/* Always render floating icon to ensure it's persistent */}
      <button className="floating-chat-icon" onClick={toggleChat} aria-label="Open chat">
        <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>
    </>
  );
};

export default FloatingChatIcon;
