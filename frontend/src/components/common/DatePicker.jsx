import './Input.css';

function DatePicker({ label, id, value, onChange, required = false, disabled = false, error, className = '' }) {
  return (
    <div className={`input-group ${className}`}>
      {label && (
        <label htmlFor={id} className="input-label">
          {label}
          {required && <span className="input-required">*</span>}
        </label>
      )}
      <input
        id={id}
        type="date"
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        className={`input-field ${error ? 'input-field--error' : ''}`}
      />
      {error && <span className="input-error">{error}</span>}
    </div>
  );
}

export default DatePicker;
