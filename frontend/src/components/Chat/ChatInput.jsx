import { useState, useEffect } from 'react';
import './ChatInput.css';

function ChatInput({ onSend, loading, prefill = '' }) {
  const [message, setMessage] = useState('');

  // When prefill changes (from suggestion button click), set the input
  useEffect(() => {
    if (prefill) {
      setMessage(prefill);
    }
  }, [prefill]);

  const handleSend = () => {
    if (message.trim() && !loading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Describe your HCP interaction..."
        rows={2}
        className="chat-input__textarea"
        disabled={loading}
        id="chat-input-textarea"
      />
      <button
        onClick={handleSend}
        disabled={!message.trim() || loading}
        className="chat-input__send"
        id="chat-send-btn"
        title="Send message"
      >
        {loading ? (
          <span className="chat-input__spinner" />
        ) : (
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M16 2L8.5 9.5M16 2l-5 14-2.5-6.5L2 7l14-5z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </button>
    </div>
  );
}

export default ChatInput;
