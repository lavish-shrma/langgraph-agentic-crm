import { useSelector } from 'react-redux';
import './AISuggestedFollowUps.css';

function AISuggestedFollowUps() {
  const suggestions = useSelector((state) => state.interaction.ai_suggested_followups);

  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="ai-suggestions">
      <div className="ai-suggestions__header">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M8 1l2 3h3l-2.5 2.5L12 10l-4-2-4 2 1.5-3.5L3 4h3l2-3z" fill="#2563eb"/>
        </svg>
        <span className="ai-suggestions__title">AI Suggested Follow-ups</span>
      </div>
      <div className="ai-suggestions__chips">
        {suggestions.map((suggestion, index) => (
          <div key={index} className="ai-suggestions__chip animate-fade-in">
            {suggestion}
          </div>
        ))}
      </div>
    </div>
  );
}

export default AISuggestedFollowUps;
