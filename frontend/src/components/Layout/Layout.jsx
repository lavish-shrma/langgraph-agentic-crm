import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';
import './Layout.css';

function Layout({ children }) {
  return (
    <div className="layout">
      <Header />
      <div className="layout__body">
        <Sidebar />
        <main className="layout__content">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
