import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import { trackPageView } from './utils/analytics';
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
    // Track page view on app load
    trackPageView('ACRRM Training Map', {
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    });

    // Load training sites data - now using full dataset with 921+ sites
    // Use import.meta.env.BASE_URL to work with both dev and GitHub Pages
    const basePath = import.meta.env.BASE_URL;
    fetch(`${basePath}data/training-sites-full.json`)
      .then(response => response.json())
      .then(data => {
        // Data is already an array, not nested under trainingSites
        // Generate IDs for sites that don't have them
        const sitesWithIds = data.map((site, index) => ({
          ...site,
          id: site.id || `site-${index}`
        }));
        setSites(sitesWithIds);

        // Track data load event
        trackPageView('Data Loaded', {
          siteCount: sitesWithIds.length
        });
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
