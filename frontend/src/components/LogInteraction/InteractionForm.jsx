import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setField, submitInteraction, resetForm, clearSubmitStatus } from '../../store/interactionSlice.js';
import HcpSearch from './HcpSearch.jsx';
import SampleEntry from './SampleEntry.jsx';
import SentimentSelector from './SentimentSelector.jsx';
import FollowUpSection from './FollowUpSection.jsx';
import AISuggestedFollowUps from './AISuggestedFollowUps.jsx';
import Select from '../common/Select.jsx';
import Input from '../common/Input.jsx';
import TextArea from '../common/TextArea.jsx';
import Button from '../common/Button.jsx';
import Toast from '../common/Toast.jsx';
import { INTERACTION_TYPES } from '../../utils/constants.js';
import './InteractionForm.css';

function InteractionForm() {
  const dispatch = useDispatch();
  const interaction = useSelector((state) => state.interaction);
  const [materialsInput, setMaterialsInput] = useState('');
  const [toast, setToast] = useState(null);

  const handleFieldChange = (field) => (e) => {
    dispatch(setField({ field, value: e.target.value }));
  };

  const addMaterial = () => {
    if (materialsInput.trim()) {
      dispatch(setField({
        field: 'materials_shared',
        value: [...interaction.materials_shared, materialsInput.trim()],
      }));
      setMaterialsInput('');
    }
  };

  const removeMaterial = (index) => {
    dispatch(setField({
      field: 'materials_shared',
      value: interaction.materials_shared.filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!interaction.hcp_id) {
      setToast({ message: 'Please select an HCP first.', type: 'error' });
      return;
    }
    if (!interaction.interaction_type) {
      setToast({ message: 'Please select an interaction type.', type: 'error' });
      return;
    }
    if (!interaction.date) {
      setToast({ message: 'Please select a date.', type: 'error' });
      return;
    }

    const result = await dispatch(submitInteraction());
    if (submitInteraction.fulfilled.match(result)) {
      setToast({ message: `Interaction #${result.payload.id} saved successfully!`, type: 'success' });
      setTimeout(() => dispatch(resetForm()), 2000);
    } else {
      setToast({ message: result.payload || 'Failed to save interaction.', type: 'error' });
    }
  };

  return (
    <form className="interaction-form" onSubmit={handleSubmit}>
      <div className="interaction-form__header">
        <h2>Log New Interaction</h2>
        <p>Record your HCP visit details using the form below</p>
      </div>

      <div className="interaction-form__fields">
        {/* HCP Name */}
        <HcpSearch />

        {/* Interaction Type */}
        <Select
          label="Interaction Type"
          id="interaction-type"
          value={interaction.interaction_type}
          onChange={handleFieldChange('interaction_type')}
          options={INTERACTION_TYPES}
          placeholder="Select type..."
          required
        />

        {/* Date & Time */}
        <div className="interaction-form__row">
          <Input
            label="Date"
            id="interaction-date"
            type="date"
            value={interaction.date}
            onChange={handleFieldChange('date')}
            required
          />
          <Input
            label="Time"
            id="interaction-time"
            type="time"
            value={interaction.time}
            onChange={handleFieldChange('time')}
          />
        </div>

        {/* Attendees */}
        <Input
          label="Attendees"
          id="interaction-attendees"
          value={interaction.attendees}
          onChange={handleFieldChange('attendees')}
          placeholder="e.g., Dr. Sharma, Nurse Patel"
        />

        {/* Topics Discussed */}
        <TextArea
          label="Topics Discussed"
          id="interaction-topics"
          value={interaction.topics_discussed}
          onChange={handleFieldChange('topics_discussed')}
          placeholder="What was discussed during the interaction..."
          rows={3}
        />

        {/* Voice Note Button - Disabled */}
        <div className="interaction-form__voice-note">
          <button
            type="button"
            className="voice-note-btn"
            disabled
            title="Coming Soon"
            id="voice-note-btn"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M9 1v10M9 11a3 3 0 003-3V5a3 3 0 10-6 0v3a3 3 0 003 3zM5 8a4 4 0 008 0M9 14v3M7 17h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Voice Note
            <span className="voice-note-badge">Coming Soon</span>
          </button>
        </div>

        {/* Materials Shared */}
        <div className="materials-section">
          <label className="input-label">Materials Shared</label>
          <div className="materials-input-row">
            <input
              type="text"
              value={materialsInput}
              onChange={(e) => setMaterialsInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addMaterial(); } }}
              placeholder="Add material..."
              className="input-field"
              id="material-input"
            />
            <Button variant="secondary" size="sm" onClick={addMaterial} type="button" id="add-material-btn">
              + Add
            </Button>
          </div>
          {interaction.materials_shared.length > 0 && (
            <div className="materials-chips">
              {interaction.materials_shared.map((m, i) => (
                <span key={i} className="material-chip animate-fade-in">
                  {m}
                  <button type="button" onClick={() => removeMaterial(i)} className="material-chip__remove">✕</button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Samples */}
        <SampleEntry />

        {/* Sentiment */}
        <SentimentSelector />

        {/* Outcomes */}
        <TextArea
          label="Outcomes"
          id="interaction-outcome"
          value={interaction.outcome}
          onChange={handleFieldChange('outcome')}
          placeholder="What was the outcome of this interaction..."
          rows={2}
        />

        {/* Follow-up */}
        <FollowUpSection />

        {/* AI Suggested Follow-ups */}
        <AISuggestedFollowUps />
      </div>

      {/* Submit */}
      <div className="interaction-form__actions">
        <Button
          variant="secondary"
          type="button"
          onClick={() => {
            dispatch(resetForm());
            setMaterialsInput('');
          }}
          id="reset-form-btn"
        >
          Reset Form
        </Button>
        <Button
          variant="primary"
          type="submit"
          loading={interaction.submitting}
          id="save-interaction-btn"
        >
          Save Interaction
        </Button>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </form>
  );
}

export default InteractionForm;
