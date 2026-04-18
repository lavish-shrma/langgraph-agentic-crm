import './RadioGroup.css';

function RadioGroup({ label, id, options = [], value, onChange, required = false, className = '' }) {
  return (
    <div className={`radio-group ${className}`}>
      {label && (
        <span className="radio-group__label">
          {label}
          {required && <span className="radio-group__required">*</span>}
        </span>
      )}
      <div className="radio-group__options">
        {options.map((opt) => {
          const optValue = typeof opt === 'string' ? opt : opt.value;
          const optLabel = typeof opt === 'string' ? opt : opt.label;
          return (
            <label key={optValue} className={`radio-option ${value === optValue ? 'radio-option--active' : ''}`}>
              <input
                type="radio"
                name={id}
                value={optValue}
                checked={value === optValue}
                onChange={onChange}
                className="radio-option__input"
              />
              <span className="radio-option__indicator" />
              <span className="radio-option__label">{optLabel}</span>
            </label>
          );
        })}
      </div>
    </div>
  );
}

export default RadioGroup;
