import { useState, useRef, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { searchHCPs, setSelectedHCP, clearHCPs } from '../../store/hcpSlice.js';
import { setField } from '../../store/interactionSlice.js';
import './HcpSearch.css';

function HcpSearch() {
  const dispatch = useDispatch();
  const { hcps, loading } = useSelector((state) => state.hcp);
  const { hcp_name, hcp_id } = useSelector((state) => state.interaction);
  const [query, setQuery] = useState(hcp_name || '');
  const [showDropdown, setShowDropdown] = useState(false);
  const wrapperRef = useRef(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    setQuery(hcp_name || '');
  }, [hcp_name]);

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = useCallback((value) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (value.length >= 2) {
      debounceRef.current = setTimeout(() => {
        dispatch(searchHCPs(value));
        setShowDropdown(true);
      }, 300);
    } else {
      dispatch(clearHCPs());
      setShowDropdown(false);
    }
  }, [dispatch]);

  const handleSelect = (hcp) => {
    setQuery(hcp.name);
    dispatch(setSelectedHCP(hcp));
    dispatch(setField({ field: 'hcp_id', value: hcp.id }));
    dispatch(setField({ field: 'hcp_name', value: hcp.name }));
    dispatch(setField({ field: 'location', value: hcp.institution }));
    setShowDropdown(false);
    dispatch(clearHCPs());
  };

  return (
    <div className="hcp-search" ref={wrapperRef}>
      <label htmlFor="hcp-search-input" className="input-label">
        HCP Name<span className="input-required">*</span>
      </label>
      <div className="hcp-search__input-wrapper">
        <svg className="hcp-search__icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M7 12A5 5 0 107 2a5 5 0 000 10zM14 14l-3.5-3.5" stroke="#94a3b8" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <input
          id="hcp-search-input"
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onFocus={() => { if (hcps.length > 0) setShowDropdown(true); }}
          placeholder="Search doctor by name..."
          className="hcp-search__input"
          autoComplete="off"
        />
        {loading && <span className="hcp-search__spinner" />}
      </div>

      {showDropdown && hcps.length > 0 && (
        <ul className="hcp-search__dropdown animate-fade-in">
          {hcps.map((hcp) => (
            <li
              key={hcp.id}
              className="hcp-search__option"
              onClick={() => handleSelect(hcp)}
            >
              <div className="hcp-search__option-name">{hcp.name}</div>
              <div className="hcp-search__option-meta">
                {hcp.specialty} • {hcp.institution}
              </div>
            </li>
          ))}
        </ul>
      )}

      {showDropdown && !loading && hcps.length === 0 && query.length >= 2 && (
        <div className="hcp-search__dropdown hcp-search__empty animate-fade-in">
          No HCPs found for "{query}"
        </div>
      )}
    </div>
  );
}

export default HcpSearch;
