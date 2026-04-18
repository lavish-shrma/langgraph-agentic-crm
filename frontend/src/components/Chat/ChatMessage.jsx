import './ChatMessage.css';

function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  const time = new Date(message.timestamp).toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className={`chat-message chat-message--${isUser ? 'user' : 'assistant'} animate-fade-in`}>
      {!isUser && (
        <div className="chat-message__avatar chat-message__avatar--ai">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 1l2 3h3l-2.5 2.5L12 10l-4-2-4 2 1.5-3.5L3 4h3l2-3z" fill="#2563eb"/>
          </svg>
        </div>
      )}
      <div className="chat-message__bubble">
        <div className="chat-message__content">{message.content}</div>
        <span className="chat-message__time">{time}</span>
      </div>
    </div>
  );
}

export default ChatMessage;
