import React, { useState, useEffect } from 'react';
import Chat from './Chat';
import './FloatingChatIcon.css';

const FloatingChatIcon = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    // Ensure component is mounted before setting state
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

  // Always render the button to ensure it stays visible
  return (
    <>
      {/* Always render the chat window when open */}
      {isOpen && (
        <div className="chat-overlay" onClick={closeChat}>
          <div className="chat-window" onClick={(e) => e.stopPropagation()}>
            <div className="chat-header">
              <span>Chat Assistant</span>
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
      {/* Always render the floating icon to ensure it's persistent */}
      <button className="floating-chat-icon" onClick={toggleChat} aria-label="Open chat">
        💬
      </button>
    </>
  );
};

export default FloatingChatIcon;