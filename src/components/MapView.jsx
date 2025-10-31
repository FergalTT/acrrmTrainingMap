import React, { useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom marker icons based on training type
const createCustomIcon = (trainingTypes) => {
  let color = '#3388ff'; // Default blue

  if (trainingTypes?.includes('Core Generalist Training')) {
    color = '#28a745'; // Green for core training
  } else if (trainingTypes?.some(type => type.includes('AST'))) {
    color = '#dc3545'; // Red for AST
  }

  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });
};

const MapView = ({ sites, filters }) => {
  // Filter sites based on selected filters
  const filteredSites = useMemo(() => {
    return sites.filter(site => {
      if (filters.trainingTypes.length > 0 && !filters.trainingTypes.some(type => site.trainingTypes?.includes(type))) return false;
      if (filters.rotations.length > 0 && !filters.rotations.some(rotation => site.rotations?.includes(rotation))) return false;
      if (filters.mmm.length > 0 && !filters.mmm.includes(site.mmm)) return false;
      if (filters.siteTypes.length > 0 && !filters.siteTypes.includes(site.type)) return false;
      return true;
    });
  }, [sites, filters]);

  // Australia center coordinates
  const australiaCenter = [-25.2744, 133.7751];

  return (
    <div className="map-container">
      <MapContainer
        center={australiaCenter}
        zoom={5}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {filteredSites.map(site => (
          <Marker
            key={site.id}
            position={[site.lat, site.lng]}
            icon={createCustomIcon(site.trainingTypes)}
          >
            <Popup>
              <div className="custom-popup">
                <div className="popup-title">{site.name}</div>
                <div className="popup-info">
                  <p><strong>Location:</strong> {site.city}, {site.state}</p>
                  <p><strong>Type:</strong> <span className="badge type-badge">{site.type}</span></p>
                  {site.mmm && (
                    <p><strong>MMM:</strong> <span className={`badge mmm-${site.mmm}`}>MMM {site.mmm}</span></p>
                  )}
                  {site.status === 'Inactive' && (
                    <p><span className="badge inactive-badge">Inactive</span></p>
                  )}

                  {site.trainingTypes && (
                    <div style={{ marginTop: '8px' }}>
                      <strong>Training Types:</strong>
                      <div>
                        {site.trainingTypes.map(type => (
                          <span key={type} className="badge">{type}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {site.rotations && (
                    <div style={{ marginTop: '8px' }}>
                      <strong>Rotations:</strong>
                      <div>
                        {site.rotations.map(rotation => (
                          <span key={rotation} className="badge">{rotation}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {site.contacts && (
                    <div style={{ marginTop: '8px' }}>
                      <strong>Contacts:</strong>
                      {site.contacts.directorOfAnaesthesia && (
                        <p style={{ fontSize: '0.8rem', margin: '2px 0' }}>
                          Director: {site.contacts.directorOfAnaesthesia}
                        </p>
                      )}
                      {site.contacts.supervisors && site.contacts.supervisors.length > 0 && (
                        <p style={{ fontSize: '0.8rem', margin: '2px 0' }}>
                          Supervisors: {site.contacts.supervisors.join(', ')}
                        </p>
                      )}
                    </div>
                  )}

                  {site.associatedSites && (
                    <p style={{ marginTop: '8px' }}>
                      <strong>Associated:</strong> {site.associatedSites.join(', ')}
                    </p>
                  )}

                  {site.branchSites && (
                    <p style={{ marginTop: '8px' }}>
                      <strong>Branches:</strong> {site.branchSites.join(', ')}
                    </p>
                  )}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapView;
