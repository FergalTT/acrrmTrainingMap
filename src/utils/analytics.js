import mixpanel from 'mixpanel-browser';

// Initialize Mixpanel
const MIXPANEL_TOKEN = import.meta.env.VITE_MIXPANEL_TOKEN || '160de29a1dcd710d72e76395e7ff969d';

console.log('Initializing Mixpanel with token:', MIXPANEL_TOKEN.substring(0, 8) + '...');
console.log('Using EU data residency endpoints');

// Initialize Mixpanel on module load
mixpanel.init(MIXPANEL_TOKEN, {
  debug: true, // Always enable debug mode to see what's happening
  track_pageview: false, // We'll track page views manually
  persistence: 'localStorage', // Use localStorage for persistence
  ignore_dnt: true, // Ignore Do Not Track browser setting for testing
  // EU data residency configuration
  api_host: 'https://api-eu.mixpanel.com'
});

console.log('Mixpanel initialized successfully with EU endpoints');

/**
 * Track a custom event
 * @param {string} eventName - Name of the event to track
 * @param {Object} properties - Additional properties to track with the event
 */
export const trackEvent = (eventName, properties = {}) => {
  try {
    mixpanel.track(eventName, properties);
    console.log('Mixpanel event tracked:', eventName, properties);
  } catch (error) {
    console.error('Error tracking event:', error);
  }
};

/**
 * Track a page view
 * @param {string} pageName - Name of the page viewed
 * @param {Object} properties - Additional properties to track
 */
export const trackPageView = (pageName, properties = {}) => {
  try {
    // Use regular track instead of track_pageview for better control
    mixpanel.track('Page View', {
      page: pageName,
      url: window.location.href,
      ...properties
    });
    console.log('Mixpanel page view tracked:', pageName, properties);
  } catch (error) {
    console.error('Error tracking page view:', error);
  }
};

/**
 * Set user properties
 * @param {Object} properties - User properties to set
 */
export const setUserProperties = (properties) => {
  mixpanel.people.set(properties);
};

/**
 * Identify a user
 * @param {string} userId - Unique identifier for the user
 */
export const identifyUser = (userId) => {
  mixpanel.identify(userId);
};

/**
 * Track filter usage
 * @param {string} filterType - Type of filter used (trainingTypes, rotations, mmm, siteTypes)
 * @param {Array} selectedFilters - Array of selected filter values
 */
export const trackFilterUsage = (filterType, selectedFilters) => {
  trackEvent('Filter Applied', {
    filterType,
    selectedFilters,
    filterCount: selectedFilters.length
  });
};

/**
 * Track map interaction
 * @param {string} interactionType - Type of interaction (marker_click, zoom, pan)
 * @param {Object} details - Additional details about the interaction
 */
export const trackMapInteraction = (interactionType, details = {}) => {
  trackEvent('Map Interaction', {
    interactionType,
    ...details
  });
};

/**
 * Test function to verify Mixpanel is working
 * Call this from browser console: window.testMixpanel()
 */
export const testMixpanel = () => {
  console.log('Testing Mixpanel...');
  console.log('Token:', MIXPANEL_TOKEN.substring(0, 8) + '...');
  console.log('Mixpanel config:', mixpanel.get_config());

  trackEvent('Test Event', {
    source: 'manual_test',
    timestamp: new Date().toISOString()
  });

  console.log('Test event sent! Check your Mixpanel dashboard in a few moments.');
  console.log('Note: It may take 1-2 minutes for events to appear in Mixpanel.');
};

// Expose test function globally for console access
if (typeof window !== 'undefined') {
  window.testMixpanel = testMixpanel;
  window.mixpanelDebug = mixpanel;
}

export default mixpanel;
