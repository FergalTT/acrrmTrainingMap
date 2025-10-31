import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import './styles/App.css';

function App() {
  const [sites, setSites] = useState([]);
  const [filters, setFilters] = useState({
    trainingTypes: [],
    rotations: [],
    mmm: [],
    siteTypes: []
  });

  useEffect(() => {
    // Load training sites data - now using full dataset with 921+ sites
    fetch('/data/training-sites-full.json')
      .then(response => response.json())
      .then(data => {
        // Data is already an array, not nested under trainingSites
        // Generate IDs for sites that don't have them
        const sitesWithIds = data.map((site, index) => ({
          ...site,
          id: site.id || `site-${index}`
        }));
        setSites(sitesWithIds);
      })
      .catch(error => console.error('Error loading training sites:', error));
  }, []);

  return (
    <div className="app-container">
      <Sidebar filters={filters} setFilters={setFilters} sites={sites} />
      <MapView sites={sites} filters={filters} />
    </div>
  );
}

export default App;
