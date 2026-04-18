import { useRef, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessage } from '../../store/chatSlice.js';
import ChatMessage from './ChatMessage.jsx';
import ChatInput from './ChatInput.jsx';
import './ChatPanel.css';

function ChatPanel() {
  const dispatch = useDispatch();
  const { messages, loading } = useSelector((state) => state.chat);
  const messagesEndRef = useRef(null);
  const [prefill, setPrefill] = useState('');

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (message) => {
    setPrefill('');
    dispatch(sendMessage(message));
  };

  const handleSuggestionClick = (text) => {
    setPrefill(text);
  };

  return (
    <div className="chat-panel">
      <div className="chat-panel__header">
        <div className="chat-panel__header-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 1l3 4h4l-3.5 3.5L15 13l-5-3-5 3 1.5-4.5L3 5h4l3-4z" fill="#2563eb"/>
          </svg>
        </div>
        <div>
          <h3 className="chat-panel__title">AI Assistant</h3>
          <p className="chat-panel__subtitle">Log interaction via chat</p>
        </div>
        <div className="chat-panel__status">
          <span className="chat-panel__status-dot" />
          Online
        </div>
      </div>

      <div className="chat-panel__messages">
        {messages.length === 0 && (
          <div className="chat-panel__welcome">
            <div className="chat-panel__welcome-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="16" fill="#eff6ff"/>
                <path d="M16 8l3 5h5l-4 4 2 6-6-3-6 3 2-6-4-4h5l3-5z" fill="#2563eb"/>
              </svg>
            </div>
            <h4>How can I help you today?</h4>
            <p>Describe your HCP interaction in natural language and I'll log it for you. For example:</p>
            <div className="chat-panel__suggestions">
              <button
                className="chat-panel__suggestion"
                onClick={() => handleSuggestionClick("I met Dr. Priya Sharma at Apollo Hospital today. We discussed CardioMax efficacy. She was positive and agreed to trial it on 5 patients. I gave her 3 sample packs. Follow up in 2 weeks.")}
              >
                Log a meeting with Dr. Sharma
              </button>
              <button
                className="chat-panel__suggestion"
                onClick={() => handleSuggestionClick("Show me the profile for Dr. Priya Sharma.")}
              >
                View HCP profile
              </button>
              <button
                className="chat-panel__suggestion"
                onClick={() => handleSuggestionClick("Summarize my last 3 visits with Dr. Priya Sharma.")}
              >
                Summarize recent visits
              </button>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="chat-panel__typing animate-fade-in">
            <div className="chat-message__avatar chat-message__avatar--ai">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 1l2 3h3l-2.5 2.5L12 10l-4-2-4 2 1.5-3.5L3 4h3l2-3z" fill="#2563eb"/>
              </svg>
            </div>
            <div className="typing-indicator">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSend={handleSend} loading={loading} prefill={prefill} />
    </div>
  );
}

export default ChatPanel;
