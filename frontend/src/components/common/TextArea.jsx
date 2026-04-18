import './TextArea.css';

function TextArea({ label, id, value, onChange, placeholder, required = false, disabled = false, rows = 3, error, className = '' }) {
  return (
    <div className={`textarea-group ${className}`}>
      {label && (
        <label htmlFor={id} className="textarea-label">
          {label}
          {required && <span className="textarea-required">*</span>}
        </label>
      )}
      <textarea
        id={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        rows={rows}
        className={`textarea-field ${error ? 'textarea-field--error' : ''}`}
      />
      {error && <span className="textarea-error">{error}</span>}
    </div>
  );
}

export default TextArea;
