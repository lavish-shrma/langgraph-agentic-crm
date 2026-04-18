import './Sidebar.css';

function Sidebar() {
  const navItems = [
    { icon: '📋', label: 'Log Interaction', active: true },
    { icon: '👥', label: 'HCP Directory', active: false },
    { icon: '📊', label: 'Dashboard', active: false },
    { icon: '📅', label: 'Follow-ups', active: false },
    { icon: '📈', label: 'Reports', active: false },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar__nav">
        {navItems.map((item) => (
          <div
            key={item.label}
            className={`sidebar__item ${item.active ? 'sidebar__item--active' : ''}`}
            title={item.label}
          >
            <span className="sidebar__icon">{item.icon}</span>
            <span className="sidebar__label">{item.label}</span>
          </div>
        ))}
      </nav>
      <div className="sidebar__footer">
        <div className="sidebar__item" title="Settings">
          <span className="sidebar__icon">⚙️</span>
          <span className="sidebar__label">Settings</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
