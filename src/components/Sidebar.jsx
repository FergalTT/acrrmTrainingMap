import React, { useState } from 'react';

const Sidebar = ({ filters, setFilters, sites }) => {
  // State to track which filter sections are collapsed
  const [collapsed, setCollapsed] = useState({
    trainingTypes: true,
    rotations: true,
    mmm: true,
    siteTypes: true
  });

  const handleFilterChange = (category, value) => {
    setFilters(prev => ({
      ...prev,
      [category]: prev[category].includes(value)
        ? prev[category].filter(item => item !== value)
        : [...prev[category], value]
    }));
  };

  const handleSelectAll = (category, options) => {
    setFilters(prev => ({
      ...prev,
      [category]: prev[category].length === options.length ? [] : [...options]
    }));
  };

  const toggleCollapse = (category) => {
    setCollapsed(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const resetFilter = (category) => {
    setFilters(prev => ({
      ...prev,
      [category]: []
    }));
  };

  const clearAllFilters = () => {
    setFilters({
      trainingTypes: [],
      rotations: [],
      mmm: [],
      siteTypes: []
    });
  };

  // Extract unique values from sites
  const trainingTypes = [...new Set(sites.flatMap(site => site.trainingTypes || []))].sort();
  const rotations = [...new Set(sites.flatMap(site => site.rotations || []))].sort();
  const mmmLevels = [1, 2, 3, 4, 5, 6, 7];
  const siteTypes = [...new Set(sites.map(site => site.type))].sort();

  const filteredSitesCount = sites.filter(site => {
    if (filters.trainingTypes.length > 0 && !filters.trainingTypes.some(type => site.trainingTypes?.includes(type))) return false;
    if (filters.rotations.length > 0 && !filters.rotations.some(rotation => site.rotations?.includes(rotation))) return false;
    if (filters.mmm.length > 0 && !filters.mmm.includes(site.mmm)) return false;
    if (filters.siteTypes.length > 0 && !filters.siteTypes.includes(site.type)) return false;
    return true;
  }).length;

  return (
    <div className="sidebar">
      <h1>ACRRM Training Map</h1>

      <button className="reset-all-filters" onClick={clearAllFilters}>
        Reset All Filters
      </button>

      {/* Training Type Filter */}
      <div className="filter-section">
        <div className="filter-header">
          <h3 onClick={() => toggleCollapse('trainingTypes')} className="filter-title">
            <span className={`toggle-icon ${collapsed.trainingTypes ? 'collapsed' : 'expanded'}`}>
              {collapsed.trainingTypes ? '▶' : '▼'}
            </span>
            Training Type
            {filters.trainingTypes.length > 0 && (
              <span className="filter-count">({filters.trainingTypes.length})</span>
            )}
          </h3>
          <button
            className="reset-filter-btn"
            onClick={(e) => {
              e.stopPropagation();
              resetFilter('trainingTypes');
            }}
            disabled={filters.trainingTypes.length === 0}
          >
            Reset
          </button>
        </div>
        {!collapsed.trainingTypes && (
          <div className="filter-group">
            {trainingTypes.map(type => (
              <div key={type} className="filter-option">
                <input
                  type="checkbox"
                  id={`training-${type}`}
                  checked={filters.trainingTypes.includes(type)}
                  onChange={() => handleFilterChange('trainingTypes', type)}
                />
                <label htmlFor={`training-${type}`}>{type}</label>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Rotations Filter */}
      <div className="filter-section">
        <div className="filter-header">
          <h3 onClick={() => toggleCollapse('rotations')} className="filter-title">
            <span className={`toggle-icon ${collapsed.rotations ? 'collapsed' : 'expanded'}`}>
              {collapsed.rotations ? '▶' : '▼'}
            </span>
            Rotations
            {filters.rotations.length > 0 && (
              <span className="filter-count">({filters.rotations.length})</span>
            )}
          </h3>
          <button
            className="reset-filter-btn"
            onClick={(e) => {
              e.stopPropagation();
              resetFilter('rotations');
            }}
            disabled={filters.rotations.length === 0}
          >
            Reset
          </button>
        </div>
        {!collapsed.rotations && (
          <div className="filter-group">
            {rotations.map(rotation => (
              <div key={rotation} className="filter-option">
                <input
                  type="checkbox"
                  id={`rotation-${rotation}`}
                  checked={filters.rotations.includes(rotation)}
                  onChange={() => handleFilterChange('rotations', rotation)}
                />
                <label htmlFor={`rotation-${rotation}`}>{rotation}</label>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* MMM Level Filter */}
      <div className="filter-section">
        <div className="filter-header">
          <h3 onClick={() => toggleCollapse('mmm')} className="filter-title">
            <span className={`toggle-icon ${collapsed.mmm ? 'collapsed' : 'expanded'}`}>
              {collapsed.mmm ? '▶' : '▼'}
            </span>
            MMM Level
            {filters.mmm.length > 0 && (
              <span className="filter-count">({filters.mmm.length})</span>
            )}
          </h3>
          <button
            className="reset-filter-btn"
            onClick={(e) => {
              e.stopPropagation();
              resetFilter('mmm');
            }}
            disabled={filters.mmm.length === 0}
          >
            Reset
          </button>
        </div>
        {!collapsed.mmm && (
          <div className="filter-group">
            {mmmLevels.map(level => (
              <div key={level} className="filter-option">
                <input
                  type="checkbox"
                  id={`mmm-${level}`}
                  checked={filters.mmm.includes(level)}
                  onChange={() => handleFilterChange('mmm', level)}
                />
                <label htmlFor={`mmm-${level}`}>MMM {level}</label>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Site Type Filter */}
      <div className="filter-section">
        <div className="filter-header">
          <h3 onClick={() => toggleCollapse('siteTypes')} className="filter-title">
            <span className={`toggle-icon ${collapsed.siteTypes ? 'collapsed' : 'expanded'}`}>
              {collapsed.siteTypes ? '▶' : '▼'}
            </span>
            Site Type
            {filters.siteTypes.length > 0 && (
              <span className="filter-count">({filters.siteTypes.length})</span>
            )}
          </h3>
          <button
            className="reset-filter-btn"
            onClick={(e) => {
              e.stopPropagation();
              resetFilter('siteTypes');
            }}
            disabled={filters.siteTypes.length === 0}
          >
            Reset
          </button>
        </div>
        {!collapsed.siteTypes && (
          <div className="filter-group">
            {siteTypes.map(type => (
              <div key={type} className="filter-option">
                <input
                  type="checkbox"
                  id={`sitetype-${type}`}
                  checked={filters.siteTypes.includes(type)}
                  onChange={() => handleFilterChange('siteTypes', type)}
                />
                <label htmlFor={`sitetype-${type}`}>{type}</label>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="stats">
        <p><strong>{filteredSitesCount}</strong> of <strong>{sites.length}</strong> sites displayed</p>
      </div>
    </div>
  );
};

export default Sidebar;
