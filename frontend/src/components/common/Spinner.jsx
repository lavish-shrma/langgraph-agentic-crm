import './Spinner.css';

function Spinner({ size = 'md', className = '' }) {
  return (
    <div className={`spinner spinner--${size} ${className}`} role="status">
      <span className="sr-only">Loading...</span>
    </div>
  );
}

export default Spinner;
