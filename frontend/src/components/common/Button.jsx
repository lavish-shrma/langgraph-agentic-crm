import './Button.css';

function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  fullWidth = false,
  type = 'button',
  onClick,
  title,
  className = '',
  id,
}) {
  return (
    <button
      id={id}
      type={type}
      className={`btn btn--${variant} btn--${size} ${fullWidth ? 'btn--full' : ''} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      title={title}
    >
      {loading && <span className="btn__spinner" />}
      {children}
    </button>
  );
}

export default Button;
