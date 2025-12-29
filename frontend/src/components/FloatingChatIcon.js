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
        <svg width="32" height="32" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="robotGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1a1a2e"/>
              <stop offset="100%" stop-color="#16213e"/>
            </linearGradient>
          </defs>
          <circle cx="24" cy="24" r="22" fill="url(#robotGradient)" opacity="0.12"/>
          <rect x="12" y="20" width="24" height="20" rx="6" fill="currentColor"/>
          <circle cx="18" cy="28" r="4" fill="white" opacity="0.9"/>
          <circle cx="30" cy="28" r="4" fill="white" opacity="0.9"/>
          <rect x="22" y="8" width="4" height="6" rx="1" fill="currentColor"/>
          <rect x="26" y="42" width="12" height="3" rx="1.5" fill="currentColor"/>
          <ellipse cx="16" cy="42" rx="4" ry="3" fill="currentColor" opacity="0.6"/>
          <rect x="12" y="46" width="24" height="3" rx="1.5" fill="currentColor"/>
          <circle cx="30" cy="46" r="3" fill="white" opacity="0.9"/>
        </svg>
      </button>
    </>
  );
};

export default FloatingChatIcon;
