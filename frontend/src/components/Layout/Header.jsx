import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header__left">
        <div className="header__logo">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="28" height="28" rx="8" fill="#2563eb"/>
            <path d="M8 14h4m4 0h4M14 8v4m0 4v4" stroke="#fff" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <div className="header__title-group">
            <h1 className="header__title">HCP CRM</h1>
            <span className="header__subtitle">AI-First Platform</span>
          </div>
        </div>
      </div>
      <div className="header__right">
        <div className="header__user">
          <div className="header__avatar">FR</div>
          <div className="header__user-info">
            <span className="header__user-name">Field Representative</span>
            <span className="header__user-role">Pharma Division</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
