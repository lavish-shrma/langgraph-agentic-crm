import InteractionForm from './InteractionForm.jsx';
import ChatPanel from '../Chat/ChatPanel.jsx';
import './LogInteractionPage.css';

function LogInteractionPage() {
  return (
    <div className="log-interaction-page">
      <div className="log-interaction-page__header">
        <h1>Log Interaction</h1>
        <p>Record your HCP interaction using the form or chat with the AI assistant</p>
      </div>
      <div className="log-interaction-page__content">
        <div className="log-interaction-page__form">
          <InteractionForm />
        </div>
        <div className="log-interaction-page__chat">
          <ChatPanel />
        </div>
      </div>
    </div>
  );
}

export default LogInteractionPage;
